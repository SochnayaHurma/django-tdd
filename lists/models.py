from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings

User: AbstractUser = get_user_model()


class List(models.Model):
    """Модель содержащая поля списка дел"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              blank=True, null=True)

    def get_absolute_url(self) -> str:
        return reverse("unique-list", args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text

    @staticmethod
    def creates_new(first_item_text: str, owner: User = None):
        """
        Создает новый список
        """
        todo_list = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=todo_list)
        return todo_list


class Item(models.Model):
    """
    Модель содержащая поля элемента списка дел
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
