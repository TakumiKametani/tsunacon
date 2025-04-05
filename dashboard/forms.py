from django import forms
from .models import Project, ChatMessage, Category, Tag


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
        label="見込時間",
        max_digits=5,
        decimal_places=2,
        required=True,
        initial=5,  # 初期値を5に設定
        widget=forms.NumberInput(attrs={
            'placeholder': '5以上の時間を入力してください',
            'min': 5,  # 最小値を指定
            'step': 1  # 1ずつ増減するように設定
        })

    )

    price = forms.IntegerField(
        label="Price",
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'min': 10000})  # フロントエンドで最小値を制限
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'categories', 'tags', 'estimated_hours', 'start_date', 'end_date']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': '案件名',
            'description': '説明',
            'start_date': '開始日',
            'end_date': '終了日',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # 編集時の場合
            self.fields['tags'].queryset = Tag.objects.filter(categories__in=self.instance.categories.all())
        elif 'categories' in self.data:  # フォーム送信時（新規作成時）の場合
            category_ids = self.data.getlist('categories')
            self.fields['tags'].queryset = Tag.objects.filter(categories__id__in=category_ids)
        else:  # 初期表示時（新規作成時）
            self.fields['tags'].queryset = Tag.objects.none()

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
        if commit:
            pass


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
