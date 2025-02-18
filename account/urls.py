from django.urls import path

from . import views


app_name="account"
urlpatterns = [
    path("", views.TopView.as_view(), name="top"),
    path("login_choice/", views.LoginChoiceView.as_view(), name="login_choice"),
    path("admin_login/", views.AdminLoginView.as_view(), name="admin_login"),
    path('customer_login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('member_login/', views.MemberLoginView.as_view(), name='member_login'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # 仮登録
    path('customer_pre_registration/', views.CustomerPreRegistrationView.as_view(), name='customer_pre_registration'),
    path('member_pre_registration/', views.MemberPreRegistrationView.as_view(), name='member_pre_registration'),
    path('registration_pre_success/', views.registration_pre_success, name='registration_pre_success'),
    # 本登録
    path('customer_registration/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
    path('member_registration/', views.MemberRegistrationView.as_view(), name='member_registration'),
    path('sales_registration/', views.SalesRegistrationView.as_view(), name='sales_registration'),
    path('registration_success/', views.registration_success, name='registration_success'),
    # パスワード変更
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # パスワードリセット
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # 銀行口座登録
    path('bank_account/create/', views.BankAccountCreateView.as_view(), name='bank_account_create'),
    path('bank_account/edit/<int:pk>/', views.BankAccountEditView.as_view(), name='bank_account_edit'),
    path('bank_account/success/', views.bank_account_success, name='bank_account_success'),
    path('get_branches/', views.get_branches, name='get_branches'),
]