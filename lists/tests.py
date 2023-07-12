from django.test import TestCase


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
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')