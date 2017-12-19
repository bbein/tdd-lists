"""
Unittests for he lists APP
"""

from django.test import TestCase

from lists.models import Item, List

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

class ListAndItemModelTest(TestCase):
    """
    Test the ORM of the list APP
    """

    def test_saving_and_retriving_items(self):
        """
        Tests that we can save and retrive items from the database
        """
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

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
        
class NewListTest(TestCase):
    """
    Tests that new items and lists can be create
    """

    def test_can_save_a_POST_request(self):
        """
        tests that the homepage can save a POST request
        """
        item_text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)

    def test_redirect_after_a_POST(self):
        """
        tests that the view redirects after it did send a POST request
        """
        item_text = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text': item_text})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    """
    Tests to ensure we can add new iems to an existing list.
    """

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        tests that we can save a POST request for an existing list
        """
        correct_list = List.objects.create()
        other_list = List.objects.create()

        item_text = "A new item for an existing list"
        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': item_text})
        self.assertEqual(Item.objects.count(), 1)
        self.client.post(f'/lists/{other_list.id}/add_item', data={'item_text': item_text})

        items = Item.objects.filter(list=correct_list)
        new_item = items[0]
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """
        test that we redirect to the list view
        """
        correct_list = List.objects.create()
        other_list = List.objects.create()

        item_text = "A new item for an existing list"
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': item_text})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
