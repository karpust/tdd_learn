import django

django.setup()

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string


# Create your tests here.

class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_home_page_returns_correct_html(self):
        """тест: домашняя страница возвращает правильный html"""

        # тестируем не константы а логику:
        response = self.client.get("/")
        self.assertTemplateUsed(response=response, template_name='home.html')  # работает только для self.client

    # def test_uses_home_template(self):
    #     """тест: используется домашний шаблон"""
    #
    #     response = self.client.get('/')
    #     self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""

        # аргумент data с данными формы, которые мы хотим отправить:
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


