from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The first list item')
        self.assertEqual(saved_items[1].text, 'The second list item')

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')
        response = self.client.get('/lists/the-only-list/')
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new/', {'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new/', {'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list/')
