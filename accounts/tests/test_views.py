"""
Uint tests for the Account views
"""

from django.test import TestCase
from unittest.mock import patch
from unittest.mock import call

from accounts.models import Token

class SendLogEmailViewTest(TestCase):
    """
    Tests the send loggin email view
    """
    def test_redirects_to_home_page(self):
        """
        test that after sending the loggin email the user is redirected to the home page
        """
        response = self.client.post('/accounts/send_login_email',
                                    data={'email' : 'benbein2@gmail.com'})
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        """
        Tests that a created token is associated with an e-mail
        """
        self.client.post('/accounts/send_login_email',
                         data={'email' : 'edith@example.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """
        tests that the link the the login e-mail is created from the Token uid
        """
        self.client.post('/accounts/send_login_email',
                         data={'email' : 'edith@example.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertIn(expected_url, body)
    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """
        tests that the email is send
        """
        self.client.post('/accounts/send_login_email',
                         data={'email' : 'edith@example.com'})

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists.com')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        """
        test that a success message is displayed after a login e-mail is send
        """
        response = self.client.post('/accounts/send_login_email',
                                    data={'email': 'edith@example.com'},
                                    follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message,
                         "Check your email, we've sent you a link tou can use to log in")
        self.assertEqual(message.tags, "success")

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    """
    Tests the view of the website after the login
    """
    def test_redirects_to_home_page(self, mock_auth):
        """
        test that after sending the loggin email the user is redirected to the home page
        """
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authentication_with_uid_from_get_request(self, mock_auth):
        """
        tests that the login view calls the authentication backend with the token uid
        """
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abcd123'))

    def test_calls_authentication_with_user_if_there_is_one(self, mock_auth):
        """
        tests that the login view calls the authentication backend with the correct user
        for the token uid
        """
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.call_args,
                         call(response.wsgi_request, mock_auth.authenticate.return_value))

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        """
        tests that the user is not logedin if the user was not authenticated
        """
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertFalse(mock_auth.login.called)
