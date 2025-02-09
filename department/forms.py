from django import forms
from .models import Department, ContactPerson

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'customer']

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['name', 'email', 'phone', 'department']
