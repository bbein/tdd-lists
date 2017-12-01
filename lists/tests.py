"""
Unittests for he lists APP
"""

from django.test import TestCase

from lists.models import Item

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
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_a_post(self):
        """
        tests that the view redirects after it did send a POST request
        """
        item_text = 'A new list item'
        response = self.client.post('/', data={'item_text': item_text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_only_save_items_when_necessary(self):
        """
        tests that no item is saved in the database if we don't send one
        """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

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

class ListViewTest(TestCase):
    """
    Tests the view for a specific user list
    """
    def test_uses_list_template(self):
        """
        
        """
        response =self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        """
        tests that the website displays all list items
        """
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
