from django.contrib.auth import get_user_model
from django.conf import settings
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):
    """Базовый класс содержащий методы-фикстуры для установки состояний перед тестами"""

    def create_pre_authenticated_session(self, email: str) -> None:
        """Создает предварительно аутентифицированный сеанс"""
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email=email)
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie({
            "name": settings.SESSION_COOKIE_NAME,
            "value": session_key,
            "path": "/"
        })

    def test_logged_in_users_lists_are_saved_as_my_lists(self) -> None:
        """
        Тест: Визуально проверяем наличие списков созданных конкретным пользователем
        и отсутсвие доступа к ним неавторизованного пользователя
        """
        email = "testdjango@rambler.ru"
        first_todo_list_title = 'Reticulate splines'
        second_todo_list_title = 'Click cows'
        self.create_pre_authenticated_session(email=email)

        self.browser.get(self.live_server_url)
        self.add_list_item(first_todo_list_title)
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value=first_todo_list_title)
        )
        self.browser.find_element(by=By.LINK_TEXT, value=first_todo_list_title).click()

        self.wait_for(lambda: self.assertEqual(first_list_url, self.browser.current_url))

        self.browser.get(self.live_server_url)
        self.add_list_item(second_todo_list_title)
        second_list_url = self.browser.current_url
        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value=second_todo_list_title)
        )
        self.browser.find_element(by=By.LINK_TEXT, value=second_todo_list_title).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(by=By.LINK_TEXT, value='My lists'),
                []
            )
        )