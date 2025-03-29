from account.models import LoginStatus
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.conf import settings

from functools import wraps
from django.http import Http404


def is_admin(user):
    return user.is_superuser


def update_login_status(user, is_customer, is_member):

    # LoginStatusモデルを更新
    login_status, created = LoginStatus.objects.update_or_create(
        user=user,
        defaults={'is_customer': is_customer, 'is_member': is_member}
    )

    return login_status


def get_login_status_cache(user):
    # キャッシュキーを生成
    login_status = LoginStatus.objects.filter(
        user=user,
    ).first()
    return login_status


def with_login_status(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("User must be logged in to access this page.")

        login_status = LoginStatus.objects.filter(
            user=request.user,
        ).first()

        # リクエストオブジェクトにデータを追加
        request.login_status = login_status

        return view_func(request, *args, **kwargs)
    return wrapper