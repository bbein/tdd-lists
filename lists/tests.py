"""
Unittests for he lists APP
"""

from django.test import TestCase

class HomePageTest(TestCase):
    """
    Unit-tests for the home page
    """

    def test_home_page_returns_correct_html(self):
        """
        tests that root url resolves to home page view
        and that the home page returns the correct html
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
