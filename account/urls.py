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
    path('customer_registration_list/', views.CustomerRegistrationListView.as_view(), name='customer_registration_list'),
    path('customer_registration/edit/<int:pk>/', views.CustomerRegistrationDetailView.as_view(), name='customer_registration_detail'),
    path('member_registration_list/', views.MemberRegistrationListView.as_view(), name='member_registration_list'),
    path('member_registration/edit/<int:pk>/', views.MemberRegistrationDetailView.as_view(), name='member_registration_detail'),
    path('member_self_registration/edit/<int:pk>/', views.MemberSelfRegistrationDetailView.as_view(), name='member_self_registration_detail'),
    path('registration_success/', views.registration_success, name='registration_success'),
    # パスワード変更
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    # パスワードリセット
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # 銀行口座登録
    path('get_branches/', views.get_branches, name='get_branches'),
]