from django import forms
from .models import Project, ChatMessage, Grade


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'grade', 'estimated_hours', 'customer',
            'client_name', 'start_date', 'end_date', 'amount', 'status',
            'entry_not_allowed', 'tuna_con', 'tuna_spa'
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
            'name': 'プロジェクト名',
            'description': '説明',
            'grade': 'グレード',
            'estimated_hours': '見込時間',
            'customer': '顧客',
            'client_name': 'クライアント名',
            'start_date': '開始日',
            'end_date': '終了日',
            'amount': '金額',
            'status': 'ステータス',
            'entry_not_allowed': 'エントリ不許可',
            'tuna_con': 'ツナコン担当',
            'tuna_spa': 'ツナスパ担当',
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
