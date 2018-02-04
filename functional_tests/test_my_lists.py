"""
Functional tests to make sure that a logedin user can see all thier lists
"""
import time
import re

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth import SESSION_KEY
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import SuperListsFunctionalTest

User = get_user_model()

class MyListsTest(SuperListsFunctionalTest):
    """
    Functional test to check that all lists are displayed to a user if they are logged in
    """
    def creaate_pre_authentication_session(self, email):
        """
        creates a pre authentication session using browser cookies
        """
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## To set a cookie we need to first visit the domain.
        ## 404 pages load the quickest
        self.browser.get(self.live_server_url+"/404_no_such_url/")
        self.browser.add_cookie({'name': settings.SESSION_COOKIE_NAME,
                                 'value': session.session_key,
                                 'path':'/',
                                })

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """
        tests that a logged in user can save thier lists under my_lists
        """
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.creaate_pre_authentication_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)
        