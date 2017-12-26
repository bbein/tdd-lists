"""
Unittests for the lists APP views
"""

from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm

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

class ListViewTest(TestCase):
    """
    Tests the view for a specific user list
    """
    def test_uses_list_template(self):
        """
        tests that the user list view uses the list template
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_from_one_list(self):
        """
        tests that the website displays all list items
        """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        """
        tests that we pass the correct list to the list.html tamplate
        """
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
    
    def test_home_page_uses_item_form(self):
        """
        Tests that the home page uses the item form
        """
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):
    """
    Tests that new items and lists can be create
    """

    def test_can_save_a_POST_request(self):
        """
        tests that the homepage can save a POST request
        """
        item_text = 'A new list item'
        self.client.post('/lists/new', data={'text': item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_a_POST(self):
        """
        tests that the view redirects after it did send a POST request
        """
        item_text = 'A new list item'
        response = self.client.post('/lists/new', data={'text': item_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """
        Test that validation errors are sent back to the homepage template
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_validation_errors_are_sent_back_to_list_page_template(self):
        """
        Test that validation errors are sent back to the list page template
        """
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_are_not_saved(self):
        """
        Test that invalid items are not saved to the database
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        tests that we can save a POST request for an existing list
        """
        correct_list = List.objects.create()
        other_list = List.objects.create()

        item_text = "A new item for an existing list"
        self.client.post(f'/lists/{correct_list.id}/', data={'text': item_text})
        self.assertEqual(Item.objects.count(), 1)
        self.client.post(f'/lists/{other_list.id}/', data={'text': item_text})

        items = Item.objects.filter(list=correct_list)
        new_item = items[0]
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """
        test that we redirect to the list view
        """
        correct_list = List.objects.create()
        other_list = List.objects.create()

        item_text = "A new item for an existing list"
        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': item_text})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
