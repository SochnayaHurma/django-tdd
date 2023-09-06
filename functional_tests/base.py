from typing import Callable
from selenium.webdriver import Firefox
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = Firefox()
        # staging_server = os.environ.get('STAGING_SERVER')
        # self.live_server_url = f'http://{staging_server}'

    def tearDown(self) -> None:
        self.browser.quit()

    @staticmethod
    def wait_for(func: Callable):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text: str) -> None:
        """
        Проверка на наличии указанной в аргументе строки
        в таблице на странице
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value="id_list_table")
                rows = table.find_elements(by=By.TAG_NAME, value="tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self) -> WebElement:
        return self.browser.find_element(by=By.ID, value="id_text")
