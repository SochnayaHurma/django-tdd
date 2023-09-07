from django.test import TestCase

from lists.forms import (ItemForm, ExistingListItemForm,
                         EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR)
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


class ExistingListItemFormTest(TestCase):
    """Набор тестов проверяющих форму добавления элемента в существующий список """

    def test_form_renders_item_text_input(self) -> None:
        """Форма корректно отображает указанные атрибуты"""
        todo_list = List.objects.create()
        form = ExistingListItemForm(for_list=todo_list)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self) -> None:
        """Тест: проверка корректного заполнения атрибута errors ожидаемыми данными
        при отправке пустой формы"""
        todo_list = List.objects.create()
        form = ExistingListItemForm(for_list=todo_list, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self) -> None:
        dummy_text = "dummy dummy dummy"
        todo_list = List.objects.create()
        Item.objects.create(list=todo_list, text=dummy_text)
        form = ExistingListItemForm(for_list=todo_list, data={"text": dummy_text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
