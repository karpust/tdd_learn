from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from .base import FunctionalTest

logger = logging.getLogger(__name__)


class LayoutAndStylingTest(FunctionalTest):
    """тест макета и стилевого оформления"""

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

