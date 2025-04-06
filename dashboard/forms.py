from django import forms
from account.models import Customer
from .models import Project, ChatMessage, Category, Tag, DRAFT, REGISTRATION_COMPLETE
from utils.helper import get_login_status_cache


class ProjectForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="カテゴリー"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),  # 初期値は空
        widget=forms.CheckboxSelectMultiple,
        label="タグ",
        required=False
    )
    estimated_hours = forms.DecimalField(
        label="合計見込時間",
        max_digits=5,
        decimal_places=2,
        required=True,
        initial=5,  # 初期値を5に設定
        widget=forms.NumberInput(attrs={
            'placeholder': '5以上の時間を入力してください',
            'min': 5,  # 最小値を指定
            'step': 5  # 1ずつ増減するように設定
        })

    )

    price = forms.IntegerField(
        label="Price",
        required=False,
        widget=forms.NumberInput(attrs={
            'readonly': 'readonly',
            'min': 10000,
            'step': 1  # 小数点入力禁止
        })
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'client_name', 'categories', 'tags', 'estimated_hours', 'start_date', 'end_date']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': '案件名',
            'description': '説明',
            'client_name': 'ご担当者様',
            'start_date': '開始日',
            'end_date': '終了日',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # 編集時
            self.fields['categories'].queryset = self.instance.categories.all()
            self.fields['tags'].queryset = Tag.objects.filter(categories__in=self.instance.categories.all())
        elif 'categories' in self.data:  # 新規作成時
            category_ids = self.data.getlist('categories')
            self.fields['tags'].queryset = Tag.objects.filter(categories__id__in=category_ids)
        else:
            self.fields['tags'].queryset = Tag.objects.none()

        if self.request.login_status.is_customer:
                self.fields['client_name'] = self.request.user.last_name + ' ' + self.request.user.first_name


    def clean_estimated_hours(self):
        estimated_hours = self.cleaned_data.get('estimated_hours')
        if estimated_hours is not None and estimated_hours < 5:  # 5以上であることを確認
            raise forms.ValidationError('見込時間は5以上の値を入力してください。')
        return estimated_hours

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 10000:  # サーバー側で10000以上かを確認
            raise forms.ValidationError('価格は10000以上である必要があります。')
        return price

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.estimated_hours and instance.estimated_hours >= 5:
            instance.amount = max([a.price for a in self.cleaned_data['tags']]) * instance.estimated_hours * 2
        if 'draft' in self.request.POST:
            instance.status = DRAFT
        elif 'save' in self.request.POST:
            instance.status = REGISTRATION_COMPLETE
        if self.request.login_status.is_customer:
            instance.customer = Customer.objects.filter(user=self.request.user)
        if commit:
            instance.save()
            self.save_m2m()  # Many-to-Manyのフィールドを保存する場合
        return instance


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
