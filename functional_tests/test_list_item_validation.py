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
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEquals(
                self.browser.find_element(by=By.CLASS_NAME, value="has-error").text,
                "You can`t have an empty list item"
            )
        )

        self.browser.find_element(by=By.ID, value="id_new_item").send_keys("Buy milk")
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEquals(
            self.browser.find_element(By.CLASS_NAME, value="has-error").text,
            "You can`t have an empty list item"
        ))

        self.browser.find_element(by=By.ID, value="id_new_item").send_keys("Make tea")
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
        self.fail("Напиши меня")
