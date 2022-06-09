from unittest import skip
import unittest
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.html import escape
from django.test import TestCase
from lists.forms import *
from lists.models import Item, List
from lists.views import new_list, share_list
User = get_user_model()

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

class ListViewIntegratedTests(TestCase):
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
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
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
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_shows_error_on_list_page(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EMPTY_ITEM_ERROR_MESSAGE)

    def test_duplicate_item_error_on_list_page(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text='My text')
        response = self.client.post(f'/lists/{list1.id}/', {
            'text': 'My text'
        })
        expected_error = escape(DUPLICATE_ITEM_ERROR_MESSAGE)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)

    @skip
    def test_can_share_list(self):
        user1 = User.objects.create(email='a@example.com')
        user2 = User.objects.create(email='b@example.com')
        list_ = List.create_new(first_item_text='Eat breakfast', owner=user1)
        self.client.post(f'/lists/{list_.id}/share/', {'sharee': user2.pk})
        self.assertEqual(list_.sharees.count(), 1)
        self.assertEqual(list_.sharees.first(), user2)

@patch('lists.views.ShareForm')
class ListViewSharingUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.list_ = List.create_new(first_item_text='First item')
        self.request = HttpRequest()
        self.request.path = 'f/lists/{self.list_.id}/share/'
        self.request.POST['sharee'] = 'b@example.com'

    def test_passes_post_data_to_form(self, MockShareForm):
        share_list(self.request, list=self.list_)
        MockShareForm.assert_called_once_with(data=self.request.POST)

    def test_form_saved_if_valid(self, MockShareForm):
        mock_form = MockShareForm.return_value
        mock_form.is_valid.return_value = True
        share_list(self.request, list=self.list_)
        mock_form.save.assert_called_once_with()

    @patch('lists.views.redirect')
    def test_redirects_if_valid(self, mockRedirect, MockShareForm):
        mock_form = MockShareForm.return_value
        mock_form.is_valid.return_value = True
        response = share_list(self.request, list=self.list_)
        self.assertEqual(response, mockRedirect.return_value)
        mockRedirect.assert_called_once_with(self.list_)

    def test_does_not_save_if_invalid(self, MockShareForm):
        mock_form = MockShareForm.return_value
        mock_form.is_valid.return_value = False
        share_list(self.request, list=self.list_)
        mock_form.save.assert_not_called()

    @patch('lists.views.render')
    def test_list_object_displayed_if_invalid(self, mockRender, MockShareForm):
        mock_form = MockShareForm.return_value
        mock_form.is_valid.return_value = False
        response = share_list(self.request, list=self.list_)
        self.assertEqual(response, mockRender.return_value)
        mockRender.assert_called_once_with(self.request, 'list.html', {
            'list': self.list_,
            'form': mock_form,
        })

class NewListViewIntegratedTest(TestCase):
    def test_can_save_a_post_request(self):
        self.client.post('/lists/new/', {'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_form_invalid_input_displays_correct_error_message(self):
        response = self.client.post('/lists/new/', data={'text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR_MESSAGE)

    def test_list_owner_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new/', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)

@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new item'
        self.request.user = Mock()

    def test_passes_post_data_to_form(self, MockNewListForm):
        new_list(self.request)
        MockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, MockNewListForm):
        mock_form = MockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_object_if_form_valid(self, mockRedirect, MockNewListForm):
        mock_form = MockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)
        self.assertEqual(response, mockRedirect.return_value)
        mockRedirect.assert_called_once_with(mock_form.save.return_value)

    def test_does_not_save_if_invalid(self, MockNewListForm):
        mock_form = MockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        mock_form.save.assert_not_called()

    @patch('lists.views.render')
    def test_renders_home_if_invalid(self, mockRender, MockNewListForm):
        mock_form = MockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)
        self.assertEqual(response, mockRender.return_value)
        mockRender.assert_called_once_with(self.request, 'home.html', {
            'form': mock_form
        })

class MyListsViewTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_owner = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_owner)
