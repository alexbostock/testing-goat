from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR_MESSAGE, ItemForm
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    def post_invalid_input(self):
        list = List.objects.create()
        return self.client.post(f'/lists/{list.id}/', {
            'text': ''
        })

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_correct_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='wrong 1', list=other_list)
        Item.objects.create(text='wrong 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'wrong 1')
        self.assertNotContains(response, 'wrong 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        list = List.objects.create()
        response = self.client.get(f'/lists/{list.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(f'/lists/{correct_list.id}/', {
            'text': 'A new list item'
        })
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/', {
            'text': 'A new item for an existing list'
        })
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_shows_error_on_list_page(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EMPTY_ITEM_ERROR_MESSAGE)

class NewListTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new/', {'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new/', {'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_form_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_form_invalid_input_displays_correct_error_message(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR_MESSAGE)

    def test_form_invalid_input_uses_form_template(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'text': ''})
        self.assertEqual(Item.objects.count(), 0)
