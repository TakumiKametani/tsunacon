from datetime import datetime

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from . import forms
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http.response import JsonResponse
from .models import LoginStatus, CustomerBankAccount, MemberBankAccount

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationDetailForm, MemberRegistrationDetailForm, MemberSelfRegistrationDetailForm, OutsourcingAgreementUploadForm, ServiceUseAgreementUploadForm, ConfidentialityAgreementUploadForm

from utils.zengin_code_utils import get_branch_list
from account.models import Customer, Member, CUSTOMER_TYPES
from utils.decorator import is_self_user
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from utils.helper import update_login_status, with_login_status, is_admin


class TopView(TemplateView):
    template_name = "account/top.html"


class AdminLoginView(LoginView):
    """ログインページ"""
    form_class = forms.LoginForm
    template_name = "account/admin_login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class CustomerLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'account/customer_login.html'

    def form_valid(self, form):
        user = form.get_user()
        # ログインタイプを判別して更新
        update_login_status(user, is_customer=True, is_member=False)
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class MemberLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'account/member_login.html'

    def form_valid(self, form):
        user = form.get_user()
        # ログインタイプを判別して更新
        update_login_status(user, is_customer=False, is_member=True)
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class LoginChoiceView(TemplateView):
    template_name = "account/login_choice.html"

class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "account/logout.html"


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
            return redirect('account:registration_pre_success')
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
            return redirect('account:registration_pre_success')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


def registration_pre_success(request):
    return render(request, 'account/registration_pre_success.html')


@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CustomerRegistrationListView(View):
    template_name = 'account/customer_registration_list.html'

    def get(self, request):
        customers = Customer.objects.all()
        return render(request, self.template_name, {'customers': customers})


@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class CustomerRegistrationDetailView(UpdateView):
    model = Customer
    template_name = 'account/customer_registration.html'
    form_class = CustomerRegistrationDetailForm

    def get_context_data(self, **kwargs):
        # 既存の context データを取得
        context = super().get_context_data(**kwargs)
        # カスタムデータを追加
        context['customer'] = self.form_class(instance=self.object)  # 詳細表示用フォーム
        context['customer_types'] = CUSTOMER_TYPES
        return context

    def form_valid(self, form):
        form.instance.last_modified = datetime.now()
        form.instance.last_modifier = self.request.user
        return super(CustomerRegistrationDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account:registration_success')


@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class MemberRegistrationListView(View):
    template_name = 'account/member_registration_list.html'

    def get(self, request):
        members = Member.objects.all()
        return render(request, self.template_name, {'members': members})


@method_decorator([login_required, user_passes_test(is_admin)], name='dispatch')
class MemberRegistrationDetailView(UpdateView):
    model = Member
    template_name = 'account/member_registration.html'
    form_class = MemberRegistrationDetailForm

    def get_context_data(self, **kwargs):
        # 既存の context データを取得
        context = super().get_context_data(**kwargs)
        # カスタムデータを追加
        context['member'] = self.form_class(instance=self.object)  # 詳細表示用フォーム
        # context['customer_types'] = CUSTOMER_TYPES
        return context

    def form_valid(self, form):
        form.instance.last_modified = datetime.now()
        form.instance.last_modifier = self.request.user
        return super(MemberRegistrationDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account:registration_success')


@method_decorator([login_required, is_self_user, with_login_status], name='dispatch')
class MemberSelfRegistrationDetailView(UpdateView):
    model = Member
    template_name = 'account/member_self_registration.html'
    form_class = MemberSelfRegistrationDetailForm

    def get_context_data(self, **kwargs):
        # 既存の context データを取得
        context = super().get_context_data(**kwargs)
        # カスタムデータを追加
        context['member'] = self.form_class(instance=self.object)  # 詳細表示用フォーム
        # context['customer_types'] = CUSTOMER_TYPES
        return context

    def form_valid(self, form):
        form.instance.last_modified = datetime.now()
        form.instance.last_modifier = self.request.user
        messages.success(self.request, "更新が完了しました！")
        return super(MemberSelfRegistrationDetailView, self).form_valid(form)

    def get_success_url(self):
        # Referer（遷移元 URL）を取得
        referer_url = self.request.META.get('HTTP_REFERER')
        if referer_url and url_has_allowed_host_and_scheme(url=referer_url, allowed_hosts={self.request.get_host()}):
            return referer_url
        return reverse('account:registration_success')





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
            return redirect('account:bank_account_success')
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
            return redirect('account:bank_account_success')
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
            return redirect('account:bank_account_success')
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
            return redirect('account:bank_account_success')
        return render(request, self.template_name, {'form': form})



def bank_account_success(request):
    return render(request, 'account/bank_account_success.html')

def get_branches(request):
    bank_code = request.GET.get('bank_code')
    branches = get_branch_list(bank_code)
    return JsonResponse(branches, safe=False)

