"""
Module to unt-test forms for the list app
"""

from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item

class ItemFormTest(TestCase):
    """
    Class to thest the Item Form
    """

    def test_form_renders_item_text_input(self):
        """
        tests that the form renders the item text
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        tests that the form checks for empty entries and returns an error
        """
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_lists(self):
        """
        Tests that the form can save items to the correct list
        """
        list_ = List.objects.create()
        item_text = 'do me'
        form = ItemForm(data={'text': item_text})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, list_)