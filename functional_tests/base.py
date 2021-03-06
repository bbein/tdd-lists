"""
Functional base test calss for the Super Lists App
"""
from functools import wraps
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException

MAX_WAIT = 10

def wait_for(func):
    """
    decorater to wait for func to complete.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        wrapper needed to pass *args, **kwargs to func.
        """
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException, StaleElementReferenceException) as exc:
                if time.time() - start_time > MAX_WAIT:
                    print(time.time() - start_time)
                    raise exc
                time.sleep(0.1)
    return wrapper

class SuperListsFunctionalTest(StaticLiveServerTestCase):
    """
    Functional test class for Super Lists App.
    """

    def setUp(self):
        """
        Setup the browser and server for testing.
        """
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """
        Close the browser after testing.
        """
        self.browser.quit()

    @wait_for
    def check_for_row_in_list_table(self, row_txt):
        """
        checks if `row_text` is the text of one of the rows in the table
        """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_txt, [row.text for row in rows])
        return

    def get_item_input_box(self):
        """
        returns the input box for entering a new list item
        """
        return self.browser.find_element_by_id('id_text')

    @wait_for
    def wait_for_css_selector(self, css):
        """
        waits until it can find the css selector
        """
        return self.browser.find_element_by_css_selector(css)

    @wait_for
    def wait_for_tag_name(self, tag):
        """
        waits until it can find the tag name
        """
        return self.browser.find_element_by_tag_name(tag)

    @wait_for
    def wait_to_be_logged_in(self, email):
        """
        waits until the user is logged in
        """
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait_for
    def wait_to_be_logged_out(self, email):
        """
        waits until the user is logged out
        """
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
