from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest



# Create your tests here.

class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_root_url_resolves_to_home_page_view(self):
        """тест: корневой url преобразуется в представление домашней страницы"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """тест: домашняя страница возвращает правильный html"""
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        # сравниваем то что вернет вью и то что сделали вручную:
        self.assertEqual(html, expected_html)

        # а не тестируем константы - элементы html это и есть константы:
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.endswith('</html>'))
