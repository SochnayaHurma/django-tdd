from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    """ тест нового посетителя """

    def setUp(self):
        """ установка """
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        """ снос """
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """ тест можно начать список и получить его позже """

        # делаем гет запрос с браузера на страницу
        self.browser.get("http://localhost:8000")
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
        # ожидаем одну секунду
        time.sleep(2)
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')

        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        # получаем объект элемента таблицы по атрибуту id
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        # через объект таблицы пытаемся получить доступ к дочерним элементам tr
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        # перебираем найденные строки и ищем ожидаемую
        self.assertIn(
            '1: Купить павлиньи перья',
            [row.text for row in rows]
        )
        self.assertIn(
            '2: Сделать мушку из павлиньих перьев',
            [row.text for row in rows]
        )
        # провоцируем фэйл теста т.к приложение еще не завершено
        self.fail("Закончить тест!")


if __name__ == "__main__":
    unittest.main()
