from django.contrib.auth import get_user_model, BACKEND_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

from .base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):
    """Базовый класс содержащий методы-фикстуры для установки состояний перед тестами"""

    def create_pre_authenticated_session(self, email: str) -> User:
        """Фикстура авторизующая пользователя в атрибуте объекта браузера self.brauser"""
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie({
            "name": settings.SESSION_COOKIE_NAME,
            "value": session.session_key,
            "path": "/"
        })
        return user

    def test_logged_in_users_lists_are_saved_as_my_lists(self) -> None:
        email = "bentadjik@gmail.com"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=email)
        # Заходим на домашнюю страницу и убеждаемся, что мы неаутентифицированный пользователь

        self.create_pre_authenticated_session(email=email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=email)
        # Создаем сессию в браузере и убеждаемся что мы аутентифицированы


