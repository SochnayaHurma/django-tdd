from django.test import TestCase

from lists.models import Item


class HomePagetest(TestCase):
    """ тест домашней страницы """

    def test_home_page_returns_correct_html(self):
        """
        Тест на возвращаемый html домашней страницей
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """
        Тест: пробует отправить POST запрос и получить в теле ответа отправленную запись
        """
        response = self.client.post("/", data={
            'item_text': 'A new list item'
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertIn(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        Тест: на переадресацию после POST запроса
        """
        response = self.client.post("/", data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        """
        Тест сохрраняет элементы только когда нужно
        """
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/')

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())


class ListModelTest(TestCase):
    """
    Тест модели списка
    """

    def test_saving_and_retrieving_items(self):
        """
        Тест: сохранения и получения элементов списка
        """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')