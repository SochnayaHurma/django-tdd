from django.db import models


class List(models.Model):
    """Модель содержащая поля списка дел"""


class Item(models.Model):
    """
    Модель содержащая поля элемента списка дел
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
