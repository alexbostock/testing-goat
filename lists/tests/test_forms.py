from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR_MESSAGE
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
