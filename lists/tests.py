"""
Unittests for he lists APP
"""

from django.test import TestCase

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
