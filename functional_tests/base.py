"""
Functional base test calss for the Super Lists App
"""

import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

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

    def check_for_row_in_list_table(self, row_txt):
        """
        checks if `row_text` is the text of one of the rows in the table
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_txt, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as exc:
                if time.time() - start_time > MAX_WAIT:
                    raise exc
                time.sleep(0.1)
