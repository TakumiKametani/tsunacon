from django import forms
from .models import Department, Person

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'customer']

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'phone',
            'notification_email',
            'department'
        ]
