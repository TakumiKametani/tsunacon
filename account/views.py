from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import forms
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import JsonResponse
from .models import LoginStatus, CustomerBankAccount, MemberBankAccount

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationForm, MemberRegistrationForm, OutsourcingAgreementUploadForm, ServiceUseAgreementUploadForm, ConfidentialityAgreementUploadForm

from utils.zengin_code_utils import get_branch_list


class TopView(TemplateView):
    template_name = "account/top.html"


class AdminLoginView(LoginView):
    """ログインページ"""
    form_class = forms.LoginForm
    template_name = "account/admin_login.html"


class CustomerLoginView(LoginView):
    template_name = 'account/customer_login.html'

    def form_valid(self, form):
        user = form.get_user()
        # ログインタイプを判別して更新
        LoginStatus.objects.update_or_create(user=user, defaults={'is_customer': True, 'is_member': False})
        return redirect(self.get_success_url())


class MemberLoginView(LoginView):
    template_name = 'account/member_login.html'

    def form_valid(self, form):
        user = form.get_user()
        # ログインタイプを判別して更新
        LoginStatus.objects.update_or_create(user=user, defaults={'is_customer': False, 'is_member': True})
        return redirect(self.get_success_url())


class LoginChoiceView(TemplateView):
    template_name = "account/login_choice.html"

class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "account/admin_login.html"


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    form_class = forms.CustomPasswordChangeForm
    success_url = '/account/password-change-done/'

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = forms.CustomPasswordResetForm
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_url = '/account/password-reset-done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = '/account/password-reset-complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class CustomerPreRegistrationView(View):
    template_name = 'account/customer_pre_registration.html'

    def get(self, request):
        form = forms.CustomerPreRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.CustomerPreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
        return render(request, self.template_name, {'form': form})


class MemberPreRegistrationView(View):
    template_name = 'account/member_pre_registration.html'

    def get(self, request):
        form = forms.MemberPreRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.MemberPreRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
        return render(request, self.template_name, {'form': form})


def registration_pre_success(request):
    return render(request, 'account/registration_pre_success.html')


def is_admin(user):
    return user.is_superuser

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CustomerRegistrationView(View):
    template_name = 'account/customer_registration.html'

    def get(self, request):
        form = CustomerRegistrationForm()
        service_use_contract_form = ServiceUseAgreementUploadForm()
        return render(
            request, self.template_name,
            {
                'form': form,
                'service_use_contract_form': service_use_contract_form,
            }
        )

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        service_use_contract_form = ServiceUseAgreementUploadForm(request.POST, request.FILES)

        if form.is_valid():
            customer = form.save(commit=False)
            if service_use_contract_form.is_valid():
                contract = service_use_contract_form.save()
                customer.service_use_contract = contract
            customer.save()
            return redirect('registration_success')
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'service_use_contract_form': service_use_contract_form
            }
        )

@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class MemberRegistrationView(View):
    template_name = 'account/member_registration.html'

    def get(self, request):
        form = MemberRegistrationForm()
        outsourcing_contract_form = OutsourcingAgreementUploadForm()
        service_use_contract_form = ServiceUseAgreementUploadForm()
        confidentiality_contract_form = ConfidentialityAgreementUploadForm()
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'outsourcing_contract_form': outsourcing_contract_form,
                'service_use_contract_form': service_use_contract_form,
                'confidentiality_contract_form': confidentiality_contract_form
            }
        )

    def post(self, request):
        form = MemberRegistrationForm(request.POST)
        outsourcing_contract_form = OutsourcingAgreementUploadForm()
        service_use_contract_form = ServiceUseAgreementUploadForm()
        confidentiality_contract_form = ConfidentialityAgreementUploadForm()
        if form.is_valid():
            member = form.save(commit=False)
            if service_use_contract_form.is_valid():
                contract = service_use_contract_form.save()
                member.service_use_contract = contract
            if outsourcing_contract_form.is_valid():
                contract = outsourcing_contract_form.save()
                member.outsourcing_contract = contract
            if confidentiality_contract_form.is_valid():
                contract = confidentiality_contract_form.save()
                member.confidentiality_contract = contract
            member.save()
            return redirect('registration_success')
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'outsourcing_contract_form': outsourcing_contract_form,
                'service_use_contract_form': service_use_contract_form,
                'confidentiality_contract_form': confidentiality_contract_form
            }
        )


def registration_success(request):
    return render(request, 'account/registration_success.html')


class CustomerBankAccountCreateView(View):
    template_name = 'account/bank_account_form.html'

    def get(self, request):
        form = forms.CustomerBankAccountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.CustomerBankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.save()
            return redirect('bank_account_success')
        return render(request, self.template_name, {'form': form})

class CustomerBankAccountEditView(View):
    template_name = 'account/bank_account_form.html'

    def get(self, request, pk):
        bank_account = CustomerBankAccount.objects.get(pk=pk, user=request.user)
        form = forms.CustomerBankAccountForm(instance=bank_account)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = forms.CustomerBankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.save()
            return redirect('bank_account_success')
        return render(request, self.template_name, {'form': form})


class MemberBankAccountCreateView(View):
    template_name = 'account/bank_account_form.html'

    def get(self, request):
        form = forms.MemberBankAccountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.MemberBankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.save()
            return redirect('bank_account_success')
        return render(request, self.template_name, {'form': form})

class MemberBankAccountEditView(View):
    template_name = 'account/bank_account_form.html'

    def get(self, request, pk):
        bank_account = MemberBankAccount.objects.get(pk=pk, user=request.user)
        form = forms.MemberBankAccountForm(instance=bank_account)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        form = forms.MemberBankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.save()
            return redirect('bank_account_success')
        return render(request, self.template_name, {'form': form})



def bank_account_success(request):
    return render(request, 'account/bank_account_success.html')

def get_branches(request):
    bank_code = request.GET.get('bank_code')
    branches = get_branch_list(bank_code)
    return JsonResponse(branches, safe=False)

