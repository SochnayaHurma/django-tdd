from django.test import TestCase

from lists.models import Item, List


class HomePagetest(TestCase):
    """ тест домашней страницы """

    def test_home_page_returns_correct_html(self):
        """
        Тест на возвращаемый html домашней страницей
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
    """Тесты представления создания списка"""

    def test_can_save_a_POST_request(self):
        """
        Тест: пробует отправить POST запрос и получить в теле ответа отправленную запись
        """
        response = self.client.post("/lists/new", data={
            'item_text': 'A new list item'
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertIn(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        Тест: на переадресацию после POST запроса
        """
        response = self.client.post("/lists/new", data={'item_text': 'A new list item'})
        todo_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{todo_list.pk}/")


class ListViewTest(TestCase):
    """
    Тест представления списка дел
    """
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


class NewItemTest(TestCase):
    """Набор тестов представления добавляющего новые элементы в существующий список"""
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: Проверяет что после POST запроса запись привязывается к нужному списку"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_do_list_view(self):
        """Тест: Проверка на то, что
            1. После POST запроса произойдет redirect_status 302
            2. Нас перенаправит страницу списка дел к которому мы привязывали запись
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"}
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
