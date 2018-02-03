"""
Unit tests for the account models of the superlist app
"""

from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

User = auth.get_user_model()

class UserModelTest(TestCase):
    """
    Test the User Model.
    """
    def test_user_is_valid_with_email_only(self):
        """
        Tests that the user model is valid when only an email is known for it.
        """
        user = User(email='a@b.com')
        user.full_clean() # should not raise any errors

    def test_email_is_primary_key(self):
        """
        tests that the email is the primary Key of the database
        """
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='edith@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user) #should not raise any errors

class TokenModelTest(TestCase):
    """
    Tests the token model.
    """

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertNotEqual(token1.uid, token2.uid)
