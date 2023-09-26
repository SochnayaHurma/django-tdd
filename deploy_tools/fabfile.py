import random
import string

from fabric.api import run, local, env
from fabric.contrib.files import exists, sed, append


REPO_URL = 'https://github.com/SochnayaHurma/'


def _create_directory_structure_if_necessary(site_folder: str) -> None:
    """Принимает абсолютный путь до директории проекта и создает структуру папок если её нет"""
    directories = ('database', 'static', 'source', 'virtualenv')
    for directory in directories:
        run(f"mkdir -p {site_folder}/{directory}")


def _get_latest_source(source_folder: str) -> None:
    """По указанному в аргументе абсолютному пути клонирует актуальный коммит"""
    if exists(f"{source_folder}/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder: str, site_name: str) -> None:
    """Обращается к файлу настроек /absolute_path/settings.py и меняет настройки DEBUG, ALLOWED_HOSTS"""
    settings_path = f"{source_folder}/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$", f"ALLOWED_HOSTS = ['{site_name}']")
    secret_key_folder = f"{source_folder}/superlists/secret_key.py"
    if not exists(secret_key_folder):
        chars = f"{string.ascii_letters}{string.digits}{string.punctuation}"
        key = ''.join(random.choice(chars) for _ in range(50))
        append(secret_key_folder, f"SECRET_KEY = {key}")
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder: str, project_path: str) -> None:
    """Создает(если нету) виртуальную среду и устанавливает зависимости из requrements.txt
        предосталвенную в папке исходного кода @arg source_folder
    """
    virtualenv_folder = f"{project_path}/virtualenv"
    if not exists(f"{virtualenv_folder}/bin/pip"):
        run(f"python3 -m venv {virtualenv_folder}")
    run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(source_folder: str) -> None:
    """Функция запускает сбор статики в одну папку(collectstatic)"""
    run(f"""
    cd {source_folder} &&
    ../virtualenv/bin/python3 manage.py collectstatic --noinput
    """)


def _update_database(source_folder: str) -> None:
    run(f"""
    cd {source_folder} &&
    ../virtualenv/bin/python3 manage.py migrate --noinput
    """)


def deploy():
    """Реализует инструкцию для развертывания
        - Создает структуру директорий в проекте (если её не существует)
        - Делает git clone/fetch на актуальный коммит в вышесозданную папку
        - Обновляет константы в settings.py DEBUG, ALLOWED_HOSTS
        - Проверяет виртуальную среду(если нет установит) и устанавливает зависимости
        - Запускает сбор актуальной статики в одну папку
        - Запускает миграции базы данных
    """
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = f"{site_folder}/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder, site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

