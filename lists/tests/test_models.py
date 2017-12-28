"""
Unittests for the lists APP data Models
"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

class ItemModelTest(TestCase):
    """
    Test the Item ORM implementaion of the list APP
    """

    def test_default_text(self):
        """ 
        tests that the default item text is ''
        """
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_related_list(self):
        """
        Tests that an item is related to a list
        """
        list_ = List.objects.create()
        item = Item(list=list_)
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """
        Check that saving an empty list item raises a ValidationError
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """
        Tests that the same item can not be saved to the same list
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_can_save_item_to_different_lists(self):
        """
        Tests that different lists can save the same item
        """
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() #should not raise ValidationError!

    def test_list_ordering(self):
        """
        Tests that lists are correctly ordered
        """
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representaion(self):
        """
        Tests the string representation of list items
        """
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

class ListModelTests():
    """
    Test the List ORM implementaion of the list APP
    """

    def test_get_absolute_url(self):
        """
        Tests that we can can convert a list database object into a url
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')