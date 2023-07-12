from django.db import models


class Item(models.Model):
    """
    Модель содержащая поля элемента списка дел
    """
    text = models.TextField(default='')
