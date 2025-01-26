from selenium import webdriver
import unittest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """демонтаж"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список и получить его позже"""

        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел:
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья"
        inputbox.send_keys('Купить павлиньи перья')  # вводит
        inputbox.send_keys(Keys.ENTER)  # Keys съест и ctrl
        time.sleep(1)  # явное ожидание - гарантирует, что браузер закончил загружать новую страницу,

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(
            any(row.text == '1: Купить павлиньи перья' for row in rows)
        )

        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
