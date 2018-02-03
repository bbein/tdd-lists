"""
Unit tests for the user authentication
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
User =get_user_model()

class AuthenticationTest(TestCase):
    """
    Unit test for user authentication using an authentication token
    """
    def test_returns_none_if_no_such_token(self):
        """
        Tests that the authentication backend returns none if the token does not exists
        """
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """
        Tests that the user with the correct email is returned if the token exists
        """
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEquals(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """
        tests that the correct user for the token is returned if the user already exists
        """
        email = 'edith@example.com'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEquals(user, existing_user)

class GetUserTest(TestCase):
    """
    tests the authentication class get_user function
    """
    def test_gets_user_by_email(self):
        """
        tests the authentication class  get_user function can get a user using thier e-mail
        """
        User.objects.create(email='another_user@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user('edith@example.com')
        self.assertEqual(desired_user, found_user)

    def test_returns_none_if_no_user(self):
        """
        tests the authentication class get_user function returns none if no user was found
        """
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('edith@example.com'))
