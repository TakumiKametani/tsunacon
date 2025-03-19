import re
import random
import string
import uuid
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django import forms
from .models import Customer, CustomerBankAccount, MemberBankAccount, Member, OutsourcingAgreement, ConfidentialityAgreement, ServiceUseAgreement, UserType, ACCOUNT_TYPES
from utils.zengin_code_utils import get_bank_list, get_branch_list
from utils.validators import validate_katakana
from django.contrib.auth import authenticate
from account.models import CustomUser


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
    """ログインフォーム"""
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'name@example.com',
        'autofocus': True
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'floatingPassword',
        'placeholder': 'Password'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'id': 'flexCheckDefault'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 'username' フィールドを削除
        self.fields.pop('username')
        # フィールドの順序を再設定
        self.fields['email'] = self.fields.pop('email')
        self.fields['password'] = self.fields.pop('password')
        self.fields['remember_me'] = self.fields.pop('remember_me')

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
    terms_accepted = forms.BooleanField(label='利用規約を読了しました', required=True)
    privacy_policy_accepted = forms.BooleanField(label='プライバシーポリシーを読了しました', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = _class

    class Meta:
        model = Customer
        fields = [
            'customer_type',
            'name',
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'email',
            'phone',
            'postal_code',
            'address_1',
            'address_2',
            'terms_accepted',
            'privacy_policy_accepted'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            user = CustomUser.objects.create_user(
                email=self.cleaned_data['email'],
                username=uuid.uuid4().hex[:10],
            )
            instance.user = user
            instance.terms_accepted = self.cleaned_data['terms_accepted']
            instance.privacy_policy_accepted = self.cleaned_data['privacy_policy_accepted']
            instance.user.save()
            instance.save()
        return instance


from django.core.exceptions import ValidationError

class MemberPreRegistrationForm(forms.ModelForm):
    user_type = forms.ModelChoiceField(
        label='登録タイプ',
        required=True,
        queryset=UserType.objects.all(),
        widget=forms.widgets.Select
    )
    email = forms.EmailField(label='メールアドレス', required=True)
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    terms_accepted = forms.BooleanField(label='利用規約を読了しました', required=True)
    privacy_policy_accepted = forms.BooleanField(label='プライバシーポリシーを読了しました', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = _class

    # def clean_user_type(self):
    #     user_type_str = self.cleaned_data['user_type']
    #     user_type = UserType.objects.filter(type_id=user_type_str).first()
    #     if not user_type:
    #         raise forms.ValidationError("無効な登録タイプです。")
    #     return user_type

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        email = cleaned_data.get('email')

        # CustomUserのチェック
        user = CustomUser.objects.filter(email=email).first()
        if user and Member.objects.filter(user_type=user_type, user=user).exists():
            raise ValidationError("このユーザータイプとユーザーの組み合わせはすでに登録されています。")

        return cleaned_data

    class Meta:
        model = Member
        fields = [
            'user_type',
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            'email',
            'phone',
            'postal_code',
            'address_1',
            'address_2',
            'terms_accepted',
            'privacy_policy_accepted'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            user = CustomUser.objects.create_user(
                email=self.cleaned_data['email'],
                username=uuid.uuid4().hex[:10],
            )
            instance.user = user
            instance.terms_accepted = self.cleaned_data['terms_accepted']
            instance.privacy_policy_accepted = self.cleaned_data['privacy_policy_accepted']
            instance.user.save()
            instance.save()
        return instance




class CustomerRegistrationDetailForm(forms.ModelForm):
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名', required=False)
    branch_name = forms.ChoiceField(label='支店名', required=False)
    account_type = forms.fields.ChoiceField(choices=ACCOUNT_TYPES, widget=forms.widgets.Select)
    account_number = forms.CharField(max_length=20, required=False)
    account_holder = forms.CharField(max_length=255, required=False)
    service_use_contract_file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            customer_bank = self.instance.customer_bank.filter(customer=self.instance).first()
            bank_name, branch_name, account_type, account_number, account_holder = ['']*5
            if customer_bank:
                bank_name = re.sub(r'[\(\)\',]', '', customer_bank.bank_name)
                branch_name = re.sub(r'[\(\)\',]', '', customer_bank.branch_name)
                account_type = re.sub(r'[\(\)\',]', '', customer_bank.account_type)
                account_number = re.sub(r'[\(\)\',]', '', customer_bank.account_number)
                account_holder = customer_bank.account_holder
            branch_list = get_branch_list(bank_name)
            self.fields['branch_name'].choices = branch_list
            # フィールドに初期値を設定
            self.fields['bank_name'].initial = bank_name
            self.fields['branch_name'].initial = branch_name
            self.fields['account_type'].initial = account_type
            self.fields['account_number'].initial = account_number
            self.fields['account_holder'].initial = account_holder

        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field in self.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['class'] = _class

    class Meta:
        model = Customer
        fields = [
            'customer_type',
            'name',
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
            'account_type',
            'account_number',
            'account_holder',
            'service_use_contract_file',
            'is_active',
            'is_terminated',
        ]

    def save(self, commit=True):
        customer = super().save(commit=False)
        if commit:
            customer.save()
            bank, created = CustomerBankAccount.objects.get_or_create(customer=customer)
            bank.bank_name = self.cleaned_data['bank_name'],
            bank.branch_name = self.cleaned_data['branch_name'],
            bank.account_type = self.cleaned_data['account_type'],
            bank.account_number = self.cleaned_data['account_number'],
            bank.account_holder = self.cleaned_data['account_holder']
            bank.save()
            if self.cleaned_data['service_use_contract_file']:
                ServiceUseAgreement.objects.create(
                    contract_file=self.cleaned_data['service_use_contract_file']
                )


class MemberRegistrationDetailForm(forms.ModelForm):
    last_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = forms.CharField(max_length=255, validators=[validate_katakana])
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
    branch_name = forms.ChoiceField(label='支店名')
    account_type = forms.fields.ChoiceField(choices=ACCOUNT_TYPES, widget=forms.widgets.Select)
    account_number = forms.CharField(max_length=20)
    account_holder = forms.CharField(max_length=255)
    service_use_contract_file = forms.FileField()
    confidentiality_contract_file = forms.FileField()
    outsourcing_contract_file = forms.FileField()
    user_types = forms.ModelMultipleChoiceField(queryset=UserType.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            member_bank = self.instance.member_bank.filter(customer=self.instance).first()
            bank_name = member_bank.bank_name if member_bank else '0001'
            self.fields['branch_name'].choices = get_branch_list(bank_name)
            # 関連する CustomerBankAccount を取得
            if member_bank:
                # フィールドに初期値を設定
                self.fields['bank_name'].initial = member_bank.bank_name
                self.fields['branch_name'].initial = member_bank.branch_name
                self.fields['account_type'].initial = member_bank.account_type
                self.fields['account_number'].initial = member_bank.account_number
                self.fields['account_holder'].initial = member_bank.account_holder
        _class = 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-md dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'
        for field in self.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['class'] = _class

    class Meta:
        model = Member
        fields = [
            'last_name',
            'first_name',
            'last_name_kana',
            'first_name_kana',
            # 'gender',
            'phone',
            'postal_code',
            'address_1',
            'address_2',
            'notification_email',
            'user_types',
            'referral_id',
            'bank_name',
            'branch_name',
            'account_type',
            'account_number',
            'account_holder',
            'service_use_contract_file',
            'confidentiality_contract_file',
            'outsourcing_contract_file',
            'referral_id',
            'is_active',
            'is_terminated',
        ]

    def save(self, commit=True):
        member = super().save(commit=False)
        # OutsourcingAgreement, ConfidentialityAgreement, ServiceUseAgreement
        if commit:
            member.save()
            MemberBankAccount.objects.create(
                member=member,
                bank_name=self.cleaned_data['bank_name'],
                branch_name=self.cleaned_data['branch_name'],
                account_number=self.cleaned_data['account_number'],
                account_holder=self.cleaned_data['account_holder']
            )
            if self.cleaned_data['service_use_contract_file']:
                ServiceUseAgreement.objects.create(
                    contract_file=self.cleaned_data['service_use_contract_file']
                )
            if self.cleaned_data['confidentiality_contract_file']:
                ConfidentialityAgreement.objects.create(
                    contract_file=self.cleaned_data['confidentiality_contract_file']
                )
            if self.cleaned_data['outsourcing_contract_file']:
                OutsourcingAgreement.objects.create(
                    contract_file=self.cleaned_data['outsourcing_contract_file']
                )

        return member

    def generate_unique_referral_id(self):
        while True:
            referral_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Member.objects.filter(referral_id=referral_id).exists():
                return referral_id


class OutsourcingAgreementUploadForm(forms.ModelForm):
    class Meta:
        model = OutsourcingAgreement
        fields = ['contract_file']


class ConfidentialityAgreementUploadForm(forms.ModelForm):
    class Meta:
        model = ConfidentialityAgreement
        fields = ['contract_file']


class ServiceUseAgreementUploadForm(forms.ModelForm):
    class Meta:
        model = ServiceUseAgreement
        fields = ['contract_file']


class CustomerBankAccountForm(forms.ModelForm):
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
    branch_name = forms.ChoiceField(label='支店名')

    class Meta:
        model = CustomerBankAccount
        fields = ['bank_name', 'branch_name', 'account_number', 'account_holder']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            self.fields['branch_name'].choices = get_branch_list(self.instance.bank_name)


class MemberBankAccountForm(forms.ModelForm):
    bank_name = forms.ChoiceField(choices=get_bank_list(), label='銀行名')
    branch_name = forms.ChoiceField(label='支店名')

    class Meta:
        model = MemberBankAccount
        fields = ['bank_name', 'branch_name', 'account_number', 'account_holder']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bank_name' in self.data:
            self.fields['branch_name'].choices = get_branch_list(self.data['bank_name'])
        elif self.instance.pk:
            self.fields['branch_name'].choices = get_branch_list(self.instance.bank_name)









