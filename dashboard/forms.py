from django import forms
from .models import Project, ChatMessage, Grade


class ProjectForm(forms.ModelForm):
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2, required=False)
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'grade', 'estimated_hours',
            'start_date', 'end_date'
        ]
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
            'grade': '実施内容',
            'estimated_hours': '見込時間',
            'start_date': '開始日',
            'end_date': '終了日',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['price'].initial = self.instance.grade.price
            self.fields['price'].widget.attrs['readonly'] = True


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
