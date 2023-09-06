from unittest import skip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class TestItemValidation(FunctionalTest):
    """
    Набор тестов эмулирующий некорректные вводы пользователя и реакцию на них
    """

    def test_cannot_add_empty_list_items(self):
        """Тест: Проверяет что пользователь не может создать пустой элемент списка"""
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.browser.find_element(
                by=By.CSS_SELECTOR, value="#id_text:invalid"
            )
        )

        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(
            lambda: self.browser.find_element(
                by=By.CSS_SELECTOR, value="#id_text:valid"
            )
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for(lambda: self.browser.find_element(
                By.CSS_SELECTOR, value="#id_text:invalid"
            )
        )

        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value="#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
