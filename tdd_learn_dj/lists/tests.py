import django

django.setup()

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.

class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_home_page_returns_correct_html(self):
        """тест: домашняя страница возвращает правильный html"""

        # тестируем не константы а логику:
        response = self.client.get("/")
        self.assertTemplateUsed(response=response, template_name='home.html')  # работает только для self.client

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""

        # аргумент data с данными формы, которые мы хотим отправить:
        response = self.client.post('/', data={'item_text': 'A new list item'})
        # self.assertIn('A new list item', response.content.decode())
        # self.assertTemplateUsed(response, 'home.html')

    def test_displays_all_list_items(self):
        """тест: отображаются все элементы списка"""
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    """тест модели элемента списка"""

    def test_saving_and_retrieving_items(self):
        """тест сохранения и получения элементов списка"""
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""

        # Не сохранять пустые элементы для каждого запроса
        # Код с душком: тест POST-запроса слишком длинный?
        # Показывать несколько элементов в таблице
        # Поддержка более чем одного списка!

        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        """тест: переадресует после post-запроса"""

        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')



