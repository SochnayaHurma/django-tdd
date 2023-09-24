from django.db import models
from django.contrib import auth

import uuid

# auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    """Модель содержащая поля пользователя"""

    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    """Модель содержащая поля маркера авторизации"""

    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
