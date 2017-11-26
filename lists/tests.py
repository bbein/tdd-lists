"""
Unittests for he lists APP
"""

from django.test import TestCase

from list.models import Item

class HomePageTest(TestCase):
    """
    Unit-tests for the home page
    """

    def test_uses_home_template(self):
        """
        tests that root url resolves to home page view
        and that the home page returns the correct html
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        """
        tests that the homepage can save a POST request
        """
        item_text = 'A new list item'
        response = self.client.post('/', data={'item_text': item_text})
        self.assertIn(item_text, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    """
    Test the ORM of the list APP
    """

    def test_saving_and_retriving_items(self):
        """
        Tests that we can save and retrive items from the database
        """
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
