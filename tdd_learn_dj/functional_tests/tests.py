
# import django
# django.setup()

from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
from selenium.webdriver.firefox.service import Service
import logging


logger = logging.getLogger(__name__)


class NewVisitorTest(LiveServerTestCase):
# class NewVisitorTest(StaticLiveServerTestCase):
    """тест нового посетителя"""
    MAX_WAIT = 10

    def setUp(self):
        """установка"""
        # Настроим логирование
        # logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s - %(name)s")
        logging.basicConfig(filename="test.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s - %(name)s")
        logger.info("настройка тестов setUp")
        try:
            logger.info("настройка webdriver")
            # options = webdriver.FirefoxOptions()
            options = webdriver.ChromeOptions()
            logger.info("настройка options")
            # options.binary_location = '/usr/bin/firefox'  # for ubuntu-server
            options.binary_location = '/usr/bin/google-chrome'  # for ubuntu-server
            logger.info("настройка браузера")
            # self.browser = webdriver.Firefox(service=Service(executable_path='/usr/bin/geckodriver', log_output="geckodriver.log"), options=options)
            self.browser = webdriver.Chrome(service=Service(executable_path='/usr/local/bin/chromedriver-linux64', log_output="chroomedriver.log"), options=options)
            logger.info("настройка webdriver завершена")


            staging_server = os.getenv('STAGING_SERVER')
            logger.info(f'staging_server is {staging_server}')
            if staging_server:
                self.live_server_url = 'http://' + staging_server
                logger.info(f'адрес сервера {self.live_server_url}')

            else:
                logger.error("staging_server не установлен")
            logger.info("настройка тестов setUp завершена")
        except (WebDriverException, Exception) as e:
            raise e


    def tearDown(self):
        """демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """тест: можно начать список для одного пользователя"""

        # Эдит слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        # self.browser.get('http://localhost:8000')
        logger.info(f'подключаюсь к {self.live_server_url}')
        try:
            self.browser.get(self.live_server_url)
        except (WebDriverException, Exception) as e:
            raise e
        self.assertIn('To-Do', self.browser.title)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел:
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item')

        inputbox.send_keys('Купить павлиньи перья')
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента таблицы списка
        inputbox.send_keys(Keys.ENTER)

        self.browser.get(self.live_server_url + '/lists/1/')
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        # Текствое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # self.fail('Закончить тест!')
    # Удовлетворенная, она снова ложится спать.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """тест: многочисленные пользователи могут начать списки по разным url"""

        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')

        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        # Она замечает, что ее список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь, Фрэнсис, приходит на сайт.
        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Эдит...
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        # Опять-таки, нет ни следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

    def test_layout_and_styling(self):
        """тест макета и стилевого оформления"""
        # Эдит открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # Она замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        # self.assertAlmostEqual(a, b, delta=10) — это метод unittest, который проверяет,
        # что значение 'a' примерно равно 'b' с допустимой погрешностью 'delta'.
        # inputbox.location['x'] — X-координата левого края inputbox.
        # inputbox.size['width'] / 2 — половина ширины inputbox, чтобы получить центр.
        # Проверяется, что центр inputbox находится примерно в x = 512 с допустимой погрешностью ±10 пикселей.

        # Она начинает новый список и видит, что поле ввода там тоже
        # аккуратно центировано:
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


# if __name__ == '__main__':  # тесты настроены на запуск джангой
#     unittest.main(warnings='ignore')
