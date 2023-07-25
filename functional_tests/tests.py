from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from django.test import LiveServerTestCase

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """ тест нового посетителя """

    def setUp(self):
        """ установка """
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        """ снос """
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """
        Проверка на наличие указанной в строки в таблице
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """ тест можно начать список и получить его позже """

        # делаем гет запрос с браузера на страницу
        self.browser.get(self.live_server_url)
        # проверяем что в гаоловке тега head в ответе содержится "To-Do"
        self.assertIn("To-Do", self.browser.title)
        # ищем заголовок первого уровня и пытаемся забрать его содержимое
        handler_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        # проверяем содержится ли в заголовке строка "To-Do"
        self.assertIn('To-Do', handler_text)

        # получаем объект поля ввода по атрибуту id
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        # от объекта поля сравниваем содержимое атрибута placeholder с ожидаемым
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # в объект поля ввода набираем текст
        inputbox.send_keys('Купить павлиньи перья')
        # провоцируем отправку формы регистрируя событие нажатия клавиши enter в поле ввода
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья',)

        # ожидаем одну секунду
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')

        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья',)
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
        # провоцируем фэйл теста т.к приложение еще не завершено

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        Тест: проверка что каждый пользователь получает уникальный адрес с личным списком
        """
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, value="id_new_item")
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, value='body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        input_box = self.browser.find_element(By.ID, value="id_new_item")
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEquals(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, value='body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)