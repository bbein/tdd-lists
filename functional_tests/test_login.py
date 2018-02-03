"""
Login validation tests for the Super Lists App.
"""
import time
import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from .base import SuperListsFunctionalTest

TEST_EMAIL = 'benbein2@gmail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(SuperListsFunctionalTest):
    """
    Functional test for the login to the website.
    """
    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesoe Superlists site
        # and notices a "Lo in" section in the navbar for the first time
        # It's telling her to enter her E-mail address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an E-mail has been sent
        time.sleep(1)
        self.assertIn('Check your email', self.wait_for_tag_name('body').text)

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        self.assertIn(TEST_EMAIL, self.wait_for_css_selector('.navbar').text)

        # She sees a log out button in the navbar
        self.assertIn('Log out', self.browser.find_element_by_link_text('Log out').text)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.assertNotIn(TEST_EMAIL, self.wait_for_css_selector('.navbar').text)
