from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    """
    Тест модели списка
    """

    def test_saving_and_retrieving_items(self):
        """
        Тест: сохранения и получения элементов списка
        """
        todo_list = List()
        todo_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = todo_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = todo_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, todo_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, todo_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, todo_list)

    def test_cannot_save_empty_list_items(self) -> None:
        """Тест проверяет возбуждение исключения при попытки создания пустой записи"""

        list_object = List.objects.create()
        item = Item(list=list_object, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self) -> None:
        """Тест на выдачу абсолютного пути на каждый объект модели"""
        todo_list = List.objects.create()
        self.assertEqual(todo_list.get_absolute_url(), f"/lists/{todo_list.id}/")
