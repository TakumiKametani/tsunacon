from django import forms
from .models import Ticket

class TicketRequestForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['assignee', 'project', 'num_tickets']
