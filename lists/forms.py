from django import forms
from django.db import models
from django.core.exceptions import ValidationError

from .models import Item, List

EMPTY_ITEM_ERROR = 'You can`t have an empty list item.'
DUPLICATE_ITEM_ERROR = "You`ve already got this in your list."


class ItemForm(forms.ModelForm):
    """Содержит поля формы для элемента списка"""

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
                }
            )
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class ExistingListItemForm(ItemForm):
    """Форма содержит поля элемента существующего списка модели Item"""

    def __init__(self, for_list: List, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """Проверка уникальности элементов """
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"text": [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)


class NewListForm(ItemForm):
    """
    Форма: содержит атрибуты описывающие поля необходимые для создания объекта списка
    """

    def save(self, owner):
        if owner.is_authenticated:
            return List.creates_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.creates_new(first_item_text=self.cleaned_data['text'])

