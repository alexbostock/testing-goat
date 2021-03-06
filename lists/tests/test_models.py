from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List
User = get_user_model()

class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Duplicate')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='Duplicate')
            item.full_clean()

    def test_can_save_same_item_to_separate_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        Item.objects.create(list=list_1, text='Duplicate')
        item = Item(list=list_2, text='Duplicate')
        item.full_clean()     # Should not raise Validation Error

class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_creates_new_list_and_first_item(self):
        List.create_new(first_item_text='list item')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'list item')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_adds_owner(self):
        user = User.objects.create()
        new_list = List.create_new(first_item_text='list item', owner=user)
        self.assertEqual(new_list.owner, user)

    def test_create_new_returns_newly_created_object(self):
        list_ = List.create_new(first_item_text='list item')
        new_list = List.objects.first()
        self.assertEqual(list_, new_list)

    def test_lists_can_have_owners(self):
        List(owner=User())  # Should not raise

    def test_owner_is_optional(self):
        List().full_clean() # Should not raise

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first')
        Item.objects.create(list=list_, text='second')
        self.assertEqual(list_.name, 'first')
