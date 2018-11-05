from weibo.models import User


class LoginBackends(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username, password=password)
            if user:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
