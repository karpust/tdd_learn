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

    def test_root_url_resolves_to_home_page_view(self):
        """тест: корневой url преобразуется в представление домашней страницы"""
        found = resolve('/')  # по урлу находит функцию представления
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """тест: домашняя страница возвращает правильный html"""
        response = self.client.get("/")
        html = response.content.decode('utf8')

        # а не тестируем константы - элементы html это и есть константы:
        self.assertTrue(html.startswith('<html'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response=response, template_name='home.html')  # работает только для self.client

