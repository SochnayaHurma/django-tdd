from django.core import mail
from django.conf import settings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re

from typing import Optional
import time
import poplib

from .base import FunctionalTest
from accounts.views import SUBJECT

class LoginTest(FunctionalTest):
    """Набор ФТ эмулирующих вход пользователя"""

    def wait_for_email(self, test_email: str, subject: str) -> Optional[str]:
        """
        Вспомогательная функция: отдает тело письма взависимости от константы DEBUG
        - Если DEBUG=True отдаем имитацию письма
        - Если DEBUG=False заходим на реальный электронный ящик и ищем письмо
        """
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.rambler.ru', 995)
        try:
            inbox.user(test_email)
            inbox.pass_(settings.EMAIL_HOST_PASSWORD)
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    _, lines, _ = inbox.retr(i)
                    lines = [line.decode('latin-1') for line in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
            time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self) -> None:
        """тест: пользователь регистрируется и получает уникадбну. ссыдку входа по электронной почте"""
        if self.staging_server:
            test_email = 'testdjango@rambler.ru'
        else:
            test_email = 'edit@example.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value="email").send_keys(test_email)
        self.browser.find_element(by=By.NAME, value="email").send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        ))

        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Your login link for Superlists', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body: \n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        self.wait_to_be_logged_in(email=test_email)

        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()

        self.wait_to_be_logged_out(email=test_email)

