from django.test import TestCase

from unittest.mock import Mock, patch

from lists.forms import (ItemForm, ExistingListItemForm, NewListForm,
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

    def test_form_save(self) -> None:
        """Тест: переопределенный метод .save формы корректно сохраняет данные"""
        todo_list = List.objects.create()
        form = ExistingListItemForm(for_list=todo_list, data={"text": "qweqwe"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


class NewListFormTest(TestCase):
    """
    Набор тестов проверяющих функционал класса формы
    """

    # @patch('lists.forms.List')
    # @patch('lists.forms.Item')
    # def test_save_creates_new_list_and_item_from_post_data(
    #         self, mockItem: Mock, mockList: Mock
    # ) -> None:
    #     mock_item = mockItem.return_value
    #     mock_list = mockList.return_value
    #     user = Mock()
    #
    #     form = NewListForm(data={'text': 'new item text'})
    #     form.is_valid()
    #
    #     def check_item_text_and_list() -> None:
    #         """
    #         Проверка состояние, которое должно быть перед вызовом метода .save
    #         """
    #         self.assertEqual(mock_item.text, 'new item text')
    #         self.assertEqual(mock_item.list, mock_list)
    #         self.assertTrue(mock_list.save.called)
    #
    #     mock_item.save.side_effect = check_item_text_and_list
    #
    #     form.save(owner=user)
    #     self.assertTrue(mock_item.save.called)

    @patch('lists.forms.List.creates_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
            self, mock_List_creates_new: Mock
    ) -> None:
        """
        Тест: форма корректно сохраняется если пользователь не аутентифицирован
        """
        anonymous_user = Mock(is_authenticated=False)
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()
        form.save(owner=anonymous_user)

        mock_List_creates_new.assert_called_once_with(
            first_item_text="new item text"
        )

    @patch('lists.forms.List.creates_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
            self, mock_List_create_new: Mock
    ) -> None:
        """
        Тест: в случае если пользователь аутентифицирован мы заполняем связь списка
        с объектом пользователя
        """
        user = Mock(is_authenticated=True)
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text',
            owner=user
        )

    @patch('lists.forms.List.creates_new')
    def test_save_returns_new_list_object(
            self, mock_List_creates_new: Mock) -> None:
        """
        Тест: метод save возвращает созданный объект списка
        """
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        todo_list = form.save(owner=user)
        self.assertEqual(todo_list, mock_List_creates_new.return_value)
