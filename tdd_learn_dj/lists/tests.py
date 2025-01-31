import django

django.setup()

from django.test import TestCase
from django.urls import resolve, reverse
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.

class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_uses_home_template(self):
        """тест: используется домашний шаблон"""

        response = self.client.get('/')
        # response = self.client.get(response['location'])
        self.assertTemplateUsed(response, 'home.html')


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


class ListViewTest(TestCase):
    """тест представления списка"""

    def test_displays_all_items(self):
        """тест: отображаются все элементы списка"""
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get(reverse('view_list'))
        # response = self.client.get('/lists/one_list_in_the_world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""

        response = self.client.get('/lists/one_list_in_the_world/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""

        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запроса"""

        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/one_list_in_the_world/')
        # AssertionError: 404 != 302 : Response didn't redirect as expected: Response code was 404 (expected 302)
        # вместо:
        # self.assertEqual(response.status_code, 302)  # AssertionError: 404 != 302

        # сначала не было личных списков, сначала сделаем для 1, в дальнейшем для многих:
        self.assertEqual(response['location'], '/lists/one_list_in_the_world/')



