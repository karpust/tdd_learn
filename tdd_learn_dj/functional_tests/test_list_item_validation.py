import logging
from unittest import skip

from selenium.webdriver import Keys

from .base import FunctionalTest
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)


class ItemValidationTest(FunctionalTest):
    """класс валидации элемента списка"""


    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""

        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # Домашняя страница обновляется, и появляется сообщение об ошибке,
        # которое говорит, что элементы списка не должны быть пустыми

        # обернем ассерт в лямбду, чтобы потом вызывать ф-цию:
        self.wait_for(lambda: self.assertEqual(
        self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
        "You can't have an empty list item"
        ))
        # используем лямбду для преобразования фрагмента кода,
        # который в противном случае был бы выполнен сразу, в функцию,
        # которую мы можем передавать как аргумент и которая может
        # выполняться позже и многократно.

        # используем класс CSS .has-error, чтобы отметить текст с ошибкой
        # Она пробует снова теперь с неким текстом для элемента, и теперь
        # это срабатывает
        self.fail('Закончить тест!')

