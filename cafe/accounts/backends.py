from django.contrib.auth.backends import BaseBackend
from .models import Account

class AccountBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = Account.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
