import django

django.setup()

from django.test import TestCase
from django.urls import resolve, reverse
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


# Create your tests here.

class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_uses_home_template(self):
        """тест: используется домашний шаблон"""

        response = self.client.get('/')
        # response = self.client.get(response['location'])
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'Первый (самый) элемент списка'
        first_item.list = list_
        first_item.save()
        second_item = Item()
        second_item.text = 'Элемент второй'
        second_item.list = list_

        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый (самый) элемент списка')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Элемент второй')


class ListViewTest(TestCase):
    """тест представления списка"""

    # def test_displays_all_items(self):
    #     """тест: отображаются все элементы списка"""
    #     list_ = List.objects.create()
    #     Item.objects.create(text='itemey 1', list=list_)
    #     Item.objects.create(text='itemey 2', list=list_)
    #
    #     response = self.client.get(reverse('view_list'))
    #     # response = self.client.get('/lists/one_list_in_the_world/')
    #
    #     self.assertContains(response, 'itemey 1')
    #     self.assertContains(response, 'itemey 2')
    def test_displays_only_items_for_that_list(self):
        """тест: отображаются элементы только для этого списка"""

        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='другой элемент 1 списка', list=other_list)
        Item.objects.create(text='другой элемент 2 списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'другой элемент 1 списка')
        self.assertNotContains(response, 'другой элемент 2 списка')

    # def test_uses_list_template(self):
    #     """тест: используется шаблон списка"""
    #
    #     response = self.client.get('/lists/one_list_in_the_world/')
    #     self.assertTemplateUsed(response, 'list.html')

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""

        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        """тест: передается правильный шаблон списка"""

        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


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
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}/')
        # AssertionError: 404 != 302 : Response didn't redirect as expected: Response code was 404 (expected 302)
        # вместо:
        # self.assertEqual(response.status_code, 302)  # AssertionError: 404 != 302

        # сначала не было личных списков, сначала сделаем для 1, в дальнейшем для многих:
        self.assertEqual(response['location'], f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    """тест нового элемента списка"""

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить post-запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')