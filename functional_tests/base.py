from selenium.webdriver import Firefox
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from typing import Callable
import time
import os

from .server_tools import reset_database


MAX_WAIT = 10


def wait(fn: Callable) -> Callable:
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = f'http://{self.staging_server}'
            reset_database(self.staging_server)

    def tearDown(self) -> None:
        self.browser.quit()

    @staticmethod
    @wait
    def wait_for(func: Callable):
        return func()

    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """
        Проверка на наличии указанной в аргументе строки
        в таблице на странице
        """

        table = self.browser.find_element(by=By.ID, value="id_list_table")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        """
        Вспомогательная функция: принимает Email(string)
        и визуально проверяет аутентифицирован ли он
        """
        self.browser.find_element(by=By.LINK_TEXT, value='Log out')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        """
        Вспомогательная фуннкция: принимает email(string)
        и визуально проверяет выход из системы
        """
        self.browser.find_element(by=By.NAME, value='email')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertNotIn(email, navbar.text)

    def get_item_input_box(self) -> WebElement:
        return self.browser.find_element(by=By.ID, value="id_text")

    def get_error_element(self) -> WebElement:
        return self.browser.find_element(by=By.CSS_SELECTOR, value=".has-error")

    def add_list_item(self, item_text: str) -> None:
        """
        Фикстура: добавляет указанный текст в input ввода и отправляет следом константу Enter
        для ввода
        """
        run_rows = len(self.browser.find_elements(by=By.CSS_SELECTOR, value='#id_list_table tr'))

        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f'{run_rows + 1}: {item_text}')
