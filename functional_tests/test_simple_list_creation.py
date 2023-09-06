from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class TestNewVisitor(FunctionalTest):
    """ Набор тестов эмулирующих вход нового посетителя"""

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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()

        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
        # провоцируем фэйл теста т.к приложение еще не завершено

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        Тест: проверка что каждый пользователь получает уникальный адрес с личным списком
        """
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
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

        input_box = self.get_item_input_box()
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEquals(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, value='body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

    def test_cannot_add_duplicate_items(self) -> None:
        """Тест: эмуляция пользователя добавляющего дупликат существующего элемента"""
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy wellies")

        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEquals(
            self.browser.find_element(by=By.CSS_SELECTOR, value=".has-error").text,
            "You`ve already got this in your list."
        ))
