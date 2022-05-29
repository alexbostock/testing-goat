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

    def test_form_saves_handles_saving_a_list(self):
        list_ = List.objects.create()
        form = ItemForm({'text': 'My item'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.list, list_)
        self.assertEqual(new_item.text, 'My item')

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
