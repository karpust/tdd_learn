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

