from django.test import TestCase
from django.utils.html import escape
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from lists.models import Item, List
from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR)

User: AbstractUser = get_user_model()


class HomePagetest(TestCase):
    """ тест домашней страницы """

    def test_home_page_returns_correct_html(self):
        """
        Тест на возвращаемый html домашней страницей
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self) -> None:
        """Проверяет что представление домашней страницы использую в контексте для отрисовки
            объект класса ItemForm"""
        response = self.client.get("/")
        self.assertIsInstance(response.context.get('form'), ItemForm)


class NewListTest(TestCase):
    """Тесты представления создания списка"""

    def test_can_save_a_POST_request(self):
        """
        Тест: пробует отправить POST запрос и получить в теле ответа отправленную запись
        """
        response = self.client.post("/lists/new", data={
            'text': 'A new list item'
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertIn(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        Тест: на переадресацию после POST запроса
        """
        response = self.client.post("/lists/new", data={'text': 'A new list item'})
        todo_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{todo_list.pk}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self) -> None:
        """Тест: ожидающий ошибку валидации после отправки пустого текста в форме"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = 'You can`t have an empty list item'
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self) -> None:
        """Тест: ожидает что если пост не прошел валидацию он не создаст новый объект"""

        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self) -> None:
        """При недопустимом вводе возвращает домашнюю страницу"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self) -> None:
        """Проверяет при недопустимом вводе выводит ожидаемую ошибку в шаблоне"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_input_passes_form_to_template(self) -> None:
        """При недопустимом вводе представление передает в контекст объект формы"""
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context.get("form"), ItemForm)

    def test_list_owner_is_saved_if_user_is_authenticated(self) -> None:
        """
        Тест: атрибут owner у созданного объекта списка после POST запроса заполняется
        авторизованным пользователем или null
        """
        user = User.objects.create(email='abc@mail.ru')
        self.client.force_login(user)
        self.client.post('/lists/new/', data={'text': 'new_item'})
        todo_list = List.objects.first()
        self.assertEqual(todo_list.owner, user)


class ListViewTest(TestCase):
    """
    Тест представления списка дел
    """
    def post_invalid_input(self) -> HttpResponse:
        """Метод создает объект(ORM) списка и делает POST запрос на его ID
            - возвращает объект HttpResponse
        """
        todo_list = List.objects.create()
        return self.client.post(
            f"/lists/{todo_list.pk}/",
            data={'text': ''}
        )

    def test_uses_list_template(self):
        """Проверяет что представление отдает корректный шаблон"""
        todo_list = List.objects.create()
        response = self.client.get(f'/lists/{todo_list.pk}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        """Проверяет корректность вывода созданных в бд записей на шаблон"""
        first_todo_list = List.objects.create()
        first_elem1 = Item.objects.create(text='item 1', list=first_todo_list)
        first_elem2 = Item.objects.create(text='item 2', list=first_todo_list)

        other_todo_list = List.objects.create()
        other_elem1 = Item.objects.create(text='Other item 1', list=other_todo_list)
        other_elem2 = Item.objects.create(text='Other item 2', list=other_todo_list)

        response = self.client.get(f'/lists/{first_todo_list.pk}/')
        self.assertContains(response, first_elem1.text)
        self.assertContains(response, first_elem2.text)
        self.assertNotContains(response, other_elem1.text)
        self.assertNotContains(response, other_elem2.text)

    def test_passes_correct_list_to_template(self):
        """Тест: Проверка на наличие объекта текущего списка в контексте запроса"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.pk}/")
        self.assertEqual(response.context.get("list"), correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: Проверяет что после POST запроса запись привязывается к нужному списку"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """Тест: Проверка на то, что
            1. После POST запроса произойдет redirect_status 302
            2. Нас перенаправит страницу списка дел к которому мы привязывали запись
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"}
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_for_invalid_input_nothing_saved_to_db(self) -> None:
        """Недопустимые данные в POST запросе не пораждают сущность в БД"""
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self) -> None:
        """Проверка на выдачу того же шаблона при некорректном вводе"""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self) -> None:
        """Тест: объект form корректно передается в шаблон"""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context.get("form"), ExistingListItemForm)

    def test_validation_errors_end_up_on_lists_page(self) -> None:
        """Тест: при некорректном вводе в ответе присутсвует ожидаемый текст ошибки"""
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_displays_item_form(self) -> None:
        todo_list = List.objects.create()
        response = self.client.get(f"/lists/{todo_list.pk}/")
        self.assertIsInstance(response.context.get("form"), ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self) -> None:
        """test: После попытки ввода существующего элемента ответ будет состоять из
            - ожидаемого шаблона
            - шаблон будет содержать текст предупреждения
            """
        dummy_text = "bla bla bla loremochka"
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text=dummy_text)
        response = self.client.post(f"/lists/{list1.pk}/", data={"text": dummy_text})
        expected_error = escape("You`ve already got this in your list.")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)


class MyListsTest(TestCase):
    """
    Набор тестов представления выводящего созданные пользователем списки дел
    """

    def test_my_lists_url_renders_my_lists_template(self) -> None:
        """
        Тест: на корректность вывода шаблона
        """
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self) -> None:
        """
        Тест: в контекст попадает ожидаемый объект пользователя указанный в параметре запроса
        """
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='exprected@owner.com')
        response = self.client.get(f'/lists/users/{correct_user.email}/')
        self.assertEqual(response.context["owner"], correct_user)
