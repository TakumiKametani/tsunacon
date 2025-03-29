from django.core.exceptions import PermissionDenied

def is_self_user(view_func):
    def wrapper(request, *args, **kwargs):
        member_id = kwargs.get('pk')  # URLのIDを取得
        if member_id != str(request.user.id):
            raise PermissionDenied("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper