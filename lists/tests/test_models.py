from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from unittest.mock import Mock, patch

from lists.models import Item, List


User = get_user_model()

class ListModelTest(TestCase):
    """
    Тест модели списка
    """
    def test_get_absolute_url(self) -> None:
        """Тест на выдачу абсолютного пути на каждый объект модели"""
        todo_list = List.objects.create()
        self.assertEqual(todo_list.get_absolute_url(), f"/lists/{todo_list.id}/")

    def test_create_new_creates_list_and_first_item(self) -> None:
        """
        Тест: Метод .creates_new корректно генерирует и сохраняет объект списка
        и заполняет его атрибуты указанными аргументами
        """
        text = 'new item text'
        List.creates_new(first_item_text=text)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self) -> None:
        """
        Тест: creates_new опционально сохраняет владельца если он не Анонимен
        """
        user = User.objects.create()
        List.creates_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self) -> None:
        """
        Тест: списки корректно принимают владельца в атрибут owner
        """
        List(owner=User())

    def test_list_owner_is_optional(self) -> None:
        """
        Тест: атрибут owner может быть опционален и не возбуждает исключение
        """
        List().full_clean()

    def test_create_return_new_list_object(self) -> None:
        """
        Тест: метод create_new возвращает новый объект списка
        """
        returned = List.creates_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(new_list, returned)


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

