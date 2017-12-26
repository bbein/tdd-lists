"""
Module to unt-test forms for the list app
"""

from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR

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

