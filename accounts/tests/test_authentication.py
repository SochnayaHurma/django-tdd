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


class GetUserTest(TestCase):
    """Набор тестов проверяющих функцию выдачи пользователя по PrimaryKey переданной из сессии"""

    def test_gets_user_by_email(self) -> None:
        """Тест: при существующем пользователе get_user должна корректно вернуть его объект"""
        User.objects.create(email="qwaa@gmail.com")
        email = "bentadjik@gmail.com"
        created_user = User.objects.create(email=email)
        found_user = PasswordAuthenticationBackend().get_user(email=email)
        self.assertEqual(found_user, created_user)

    def test_returns_None_if_no_user_with_that_email(self) -> None:
        """Тест: при несуществующем пользователе ожидаем None"""
        user = PasswordAuthenticationBackend().get_user(email="qwef@gmail.com")
        self.assertIsNone(user)


