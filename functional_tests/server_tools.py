from fabric.api import run
from fabric.context_managers import settings

from typing import TypeVar

Email = TypeVar("Email", bound=str)
Host = TypeVar("Host", bound=str)
SessionKey = TypeVar("SessionKey", bound=str)


def _get_manage_dot_py(host: Host) -> str:
    """Возвращает строковое представление обращения bin-файла python к модулю manage.py"""
    return "~/sites/%s/virtualenv/bin/python3 ~/sites/%s/source/manage.py" % host


def reset_database(host: Host) -> None:
    """Функция получает доступ к базе данных и очищает её"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"user@{host}"):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host: Host, email: Email) -> SessionKey:
    """Создание сеанса на сервере"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"user@{host}"):
        session_key: SessionKey = run(f"{manage_dot_py} create_session {email}")
        return session_key.strip()

