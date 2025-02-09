from django import forms
from .models import Project, ProjectHistory, ChatMessage, Grade

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'grade', 'client_name', 'client_address', 'start_date', 'end_date', 'amount']


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['project', 'message', 'is_draft']

    project_id = forms.IntegerField(widget=forms.HiddenInput())
