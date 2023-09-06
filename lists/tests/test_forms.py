from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):
    """Набор тестов проверяющих форму """

    def test_form_renders_item_text_input(self) -> None:
        """"""
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self) -> None:
        """Проверка валидации формы при получении пустого текста"""

        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors.get('text'), [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self) -> None:
        """Тест: после вызова метода .save от объекта forms появляется запись в БД"""
        todo_list = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=todo_list)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, todo_list)