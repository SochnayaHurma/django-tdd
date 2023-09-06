from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListModelTest(TestCase):
    """
    Тест модели списка
    """
    def test_get_absolute_url(self) -> None:
        """Тест на выдачу абсолютного пути на каждый объект модели"""
        todo_list = List.objects.create()
        self.assertEqual(todo_list.get_absolute_url(), f"/lists/{todo_list.id}/")


class ItemModelTest(TestCase):
    """
    Тест модели элемента списка
    """

    def test_default_text(self) -> None:
        """test: если не передать текст значение атрибута text будет пустым"""
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self) -> None:
        """test: проверка связи списка с его элементами"""
        todo_list = List.objects.create()
        item = Item()
        item.list = todo_list
        item.save()
        self.assertIn(item, todo_list.item_set.all())

    def test_cannot_save_empty_list_items(self) -> None:
        """Тест проверяет возбуждение исключения при попытки создания пустой записи"""

        list_object = List.objects.create()
        item = Item(list=list_object, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self) -> None:
        """Тест: при попытки второго элемента ожидаем ошибку ValidateionError"""
        dummy_text = "bla bla"
        todo_list = List.objects.create()
        Item.objects.create(list=todo_list, text=dummy_text)
        with self.assertRaises(ValidationError):
            item = Item(list=todo_list, text=dummy_text)
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self) -> None:
        """Тест: Уникальность записи распространяется лишь на один список"""

        dummy_text = "bla bla bla"
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text=dummy_text)
        item = Item(list=list2, text=dummy_text)
        item.full_clean()

    def test_list_ordering(self) -> None:
        """Тест: проверка упорядочивания возвращаемого из бд"""

        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="text 1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="content 3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self) -> None:
        """Тест: Строковое представление объекта должно быть равно атрибуту text"""
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")
