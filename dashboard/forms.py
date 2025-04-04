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

    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2, required=False)
    class Meta:
        model = Project
        fields = ['name', 'description', 'categories', 'tags', 'estimated_hours', 'start_date', 'end_date']

        widgets = {
            'estimated_hours': forms.NumberInput(attrs={'placeholder': '見込時間（時間単位）'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'estimated_hours': '見込時間（時間単位）',
        }
        labels = {
            'name': '案件名',
            'description': '説明',
            'category': 'カテゴリー',
            'tag': 'タグ',
            'estimated_hours': '見込時間',
            'start_date': '開始日',
            'end_date': '終了日',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # 編集時にCategoryに基づいてTagを設定
            self.fields['tags'].queryset = Tag.objects.filter(categories__in=self.instance.categories.all())

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            pass


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
