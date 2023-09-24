from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticationTest(TestCase):
    """Набор тестов проверяющих бэкенд аутентификации пользователя"""

    def test_returns_none_if_no_such_token(self) -> None:
        """Тест: ожидаем None при некорректном токене"""
        result = PasswordAuthenticationBackend().authenticate(uid="asdasd")
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self) -> None:
        """Тест: ожидаем возврат объекта пользователя при корректном токене,
            но несуществующей модели пользоватея
        """
        email = "bentadjik@gmail.com"
        token = Token.objects.create(email=email)
        user = PasswordAuthenticationBackend().authenticate(uid=token.uid)
        expected_user = User.objects.get(email=email)
        self.assertEqual(user, expected_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self) -> None:
        """Тест: при существующем пользователе и корректном uid ожидаем возврата объекта пользователя"""
        email = "bentadjik@gmail.com"
        expected_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordAuthenticationBackend().authenticate(uid=token.uid)
        self.assertEqual(expected_user, user)
