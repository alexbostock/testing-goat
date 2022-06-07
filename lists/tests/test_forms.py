import unittest
from unittest.mock import Mock, patch
from django.test import TestCase

from lists.forms import *
from lists.models import Item, List

class ItemFormTest(TestCase):
    def test_form_item_input_attributes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm({'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR_MESSAGE])

class NewListFormTest(unittest.TestCase):
    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(first_item_text='new item')

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
        self, mock_List_create_new
    ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_newly_created_list(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new_item'})
        form.is_valid()
        list_ = form.save(owner=user)
        self.assertEqual(list_, mock_List_create_new.return_value)

class ExistingListItemFormTest(TestCase):
    def test_form_item_input_attributes(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR_MESSAGE])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Duplicate!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'Duplicate!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR_MESSAGE])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'Testing'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
