import random
import string

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django import forms
from .models import Customer, BankAccount, Member, Contract, UserType
from utils.zengin_code_utils import get_bank_list, get_branch_list
from utils.validators import validate_katakana
from django.contrib.auth import authenticate



class EmailAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'your@email.com'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 'username' フィールドを削除
        self.fields.pop('username')
        # フィールドの順序を再設定
        self.fields['email'] = self.fields.pop('email')
        self.fields['password'] = self.fields.pop('password')
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "shadow-sm rounded-md w-full px-3 py-2 border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            field.widget.attrs["placeholder"] = self.add_placeholder(field_name)

    def add_placeholder(self, field_name):
        placeholders = {
            'email': 'your@email.com',
            'password': 'Enter your password',
        }
        return placeholders.get(field_name, '')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class CustomerPreRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='User Email', required=True)
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = _class

    class Meta:
        model = Customer
        fields = [
            'customer_type',
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'email',
            'phone',
            'postal_code',
            'address_1',
            'address_2'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.user.email = self.cleaned_data['user_email']
            instance.user.save()
            instance.save()
        return instance

class MemberPreRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='User Email', required=True)
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = _class

    class Meta:
        model = Member
        fields = [
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'email',
            'phone',
            'postal_code',
            'address_1',
            'address_2'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.user.email = self.cleaned_data['user_email']
            instance.user.save()
            instance.save()
        return instance


class CustomerRegistrationForm(forms.ModelForm):
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
    branch_name = forms.ChoiceField(label='支店名')
    account_number = forms.CharField(max_length=20)
    account_holder = forms.CharField(max_length=255)
    contract_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            self.fields['branch_name'].choices = get_branch_list(self.instance.bank_name)

    class Meta:
        model = Customer
        fields = [
            'customer_type',
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'phone',
            'postal_code',
            'address_1',
            'address_2',
            'notification_email',
            'billing_email',
            'payment_due_day',
            'bank_name',
            'branch_name',
            'account_number',
            'account_holder',
            'contract_file',
        ]

    def save(self, commit=True):
        member = super().save(commit=False)
        if commit:
            member.save()
            BankAccount.objects.create(
                user=member.user,
                bank_name=self.cleaned_data['bank_name'],
                branch_name=self.cleaned_data['branch_name'],
                account_number=self.cleaned_data['account_number'],
                account_holder=self.cleaned_data['account_holder']
            )
            Contract.objects.create(
                contract_file=self.cleaned_data['contract_file']
            )

class MemberRegistrationForm(forms.ModelForm):
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
    branch_name = forms.ChoiceField(label='支店名')
    account_number = forms.CharField(max_length=20)
    account_holder = forms.CharField(max_length=255)
    contract_file = forms.FileField()
    user_types = forms.ModelMultipleChoiceField(queryset=UserType.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            self.fields['branch_name'].choices = get_branch_list(self.instance.bank_name)

    class Meta:
        model = Member
        fields = [
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'phone',
            'postal_code',
            'address_1',
            'address_2',
            'notification_email',
            'user_types',
            'referral_id',
            'bank_name',
            'branch_name',
            'account_number',
            'account_holder',
            'contract_file',
            'referral_id'
        ]

    def save(self, commit=True):
        member = super().save(commit=False)
        if commit:
            member.save()
            BankAccount.objects.create(
                user=member.user,
                bank_name=self.cleaned_data['bank_name'],
                branch_name=self.cleaned_data['branch_name'],
                account_number=self.cleaned_data['account_number'],
                account_holder=self.cleaned_data['account_holder']
            )
            Contract.objects.create(
                contract_file=self.cleaned_data['contract_file']
            )
        return member

    def generate_unique_referral_id(self):
        while True:
            referral_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Member.objects.filter(referral_id=referral_id).exists():
                return referral_id

class ContractUploadForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_file']


# class BankAccountForm(forms.ModelForm):
#     bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
#     branch_name = forms.ChoiceField(label='支店名')
#
#     class Meta:
#         model = BankAccount
#         fields = ['bank_name', 'branch_name', 'account_number', 'account_holder']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'bank_name' in self.data:
#             self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
#         elif self.instance.pk:
#             self.fields['branch_name'].choices = get_branch_list(self.instance.bank_name)

