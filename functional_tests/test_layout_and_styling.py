from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest


class TestLayoutAndStyling(FunctionalTest):
    """Тест проверяющий макет и наличие стиливог оформления """

    def test_layout_and_styling(self):
        """Тест макета и стилевого оформления"""
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(by=By.ID, value="id_new_item")
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
