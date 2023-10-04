from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

User: AbstractUser = get_user_model()


class Command(BaseCommand):
    """
    Команда:
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляем аргументы текущей команде"""
        parser.add_argument('email')

    def handle(self, *args, **options) -> None:
        """Содержит действия выполняемой команды"""
        try:
            email = options["email"]
            session_key = create_pre_authenticated_session(email=email)
            self.stdout.write(session_key)
        except KeyError:
            self.stderr.write("Аргумент email является обязательным!")


def create_pre_authenticated_session(*, email: str) -> str:
    """Создаем сеанс аутентифицированного пользователя"""
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
