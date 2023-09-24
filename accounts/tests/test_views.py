from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch, call, Mock

from accounts.models import Token
from accounts.utils import add_get_params


class SendLoginEmailViewTest(TestCase):
    """Набор тестов представления send_login_email отправляющее email пользователю"""

    def test_redirects_to_home_page(self) -> None:
        """Тест: проверка, что при корректной отправке POST запроса
        произойдет редирект на домашнюю страницу"""

        response = self.client.post('/accounts/send_login_email/', data={
            "email": "bentadjik@gmail.com"
        })
        self.assertRedirects(response, "/")

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail: Mock) -> None:
        """Тест: при отправке POST запроса мы ожидаем что письмо будет отправлено"""

        self.client.post("/accounts/send_login_email/", data={
            "email": "bentadjik@gmail.com"
        })
        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), _ = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "dia_v3@rambler.ru")
        self.assertEqual(to_list, ["bentadjik@gmail.com"])

    def test_adds_success_message(self) -> None:
        """Тест: после POST запроса на получение учетной записи получаем сообщение об успехе"""
        response = self.client.post("/accounts/send_login_email/", data={
            "email": "bentadjik@gmail.com"
        }, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(
            message.message,
            "Check your email"
        )
        self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_adds_success_message_mock(self, mock_messages: Mock) -> None:
        """Тест: после POST запроса на получение учетной записи получаем сообщение об успехе"""
        expected_message = "Check your email"
        response = self.client.post("/accounts/send_login_email/", data={
            "email": "bentadjik@gmail.com"
        })
        self.assertEqual(
            mock_messages.success.call_args,
            call(response.wsgi_request, expected_message)
        )

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail: Mock) -> None:
        """Тест: в почтовом письме содержится ссылка с валидирующим токеном"""
        email = "bentadjik@gmail.com"
        self.client.post("/accounts/send_login_email/",
                         data={"email": email})
        token = Token.objects.first()
        expected_url = add_get_params(
            reverse("accounts:login"),
            token=token.uid
        )
        (_, body, _, _), _ = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """Набор тестов представления входа в систему"""

    def test_redirects_to_home_page(self, _) -> None:
        """Тест: после передачи корректного токена get параметром нас перенаправит на главную страницу"""
        response = self.client.get("/accounts/login/?token=abcd123")
        self.assertRedirects(response, "/")

    def test_creates_token_associated_with_email(self, _) -> None:
        """Тест: после POST запроса на представление send_login_email создается токен
            привязанный к адресу указанному в запросе
        """
        email = "bentadjik@gmail.com"
        self.client.post("/accounts/send_login_email/",
                                    data={"email": email})
        token = Token.objects.first()
        self.assertEqual(token.email, email)

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth: Mock) -> None:
        token = "qweasd"
        self.client.get(f"/accounts/login/?token={token}")
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid=token)
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth: Mock) -> None:
        """
        Тест: функция login в представлении авторизации получила аргумент
        объекта пользователя из функции authenticate
        """
        response = self.client.get('/accounts/login/?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth: Mock) -> None:
        """
        Тест: если при авторизации было возвращено None мы ожидаем что функция login не бдует вызвана
        """
        mock_auth.authenticate.return_value = None
        self.client.get("/accounts/login/?token=abcd123")
        self.assertFalse(
            mock_auth.login.called
        )
