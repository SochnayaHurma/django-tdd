from django.contrib.auth import get_user_model
from django.http import HttpRequest

from typing import Optional

from .models import Token


User = get_user_model()


class PasswordAuthenticationBackend:
    """Бэкэнд содержащий функционал для авторизации пользователя """

    @staticmethod
    def authenticate(request: HttpRequest = None, uid: str = None) -> Optional[User]:
        """Функция авторизующая пользователя по аргументу uid
            return
            - None при ненайденом uid
            - user при корректному uid
        """
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    @staticmethod
    def get_user(email: str) -> Optional[User]:
        """Метод выдает пользователя при корректных данных иначе None"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
