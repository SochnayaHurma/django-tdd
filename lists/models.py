from django.db import models
from django.urls import reverse


class List(models.Model):
    """Модель содержащая поля списка дел"""

    def get_absolute_url(self) -> str:
        return reverse("unique-list", args=[self.id])


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
