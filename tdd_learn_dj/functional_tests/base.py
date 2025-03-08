from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
from selenium.webdriver.chrome.service import Service
import logging


logger = logging.getLogger(__name__)

class FunctionalTest(StaticLiveServerTestCase):
    """функциональный тест"""
    def __init__(self):
        super().__init__()
        self.max_wait = 10


    def setUp(self):
        """установка"""
        # Настроим логирование
        # logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s - %(name)s")
        logging.basicConfig(filename="test.log", level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s - %(name)s")
        logger.info("настройка тестов setUp")
        try:
            logger.info("настройка webdriver")
            # options = webdriver.FirefoxOptions()
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--headless")  # Запуск без GUI
            self.options.add_argument("--disable-gpu")  # Отключение GPU
            self.options.add_argument("--no-sandbox")  # Отключение песочницы
            self.options.add_argument("--disable-dev-shm-usage")  # Для избежания проблем с памятью
            logger.info("настройка options")
            # options.binary_location = '/usr/bin/firefox'  # for ubuntu-server
            self.options.binary_location = '/usr/bin/google-chrome'  # for ubuntu-server
            logger.info("настройка браузера")
            # self.browser = webdriver.Firefox(service=Service(executable_path='/usr/bin/geckodriver', log_output="geckodriver.log"), options=options)
            self.service = Service(executable_path='/usr/local/bin/chromedriver-linux64/chromedriver',
                                   log_output="chromedriver.log")
            self.browser = webdriver.Chrome(service=self.service, options=self.options)
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
                if time.time() - start_time > self.max_wait:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        """ожидать"""
        """
        запускает ассерт обернутый в лямбду;
        если выкинет исключение, то подождет и опять попробует,
        если выполнится то покинет цикл благодяря return
        """

        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.max_wait:
                    raise e
                time.sleep(0.5)



# if __name__ == '__main__':  # тесты настроены на запуск джангой
#     unittest.main(warnings='ignore')
