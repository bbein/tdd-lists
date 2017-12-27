"""
Input validation tests for the Super Lists App.
"""
from unittest import skip
from time import sleep

from selenium.webdriver.common.keys import Keys

from .base import SuperListsFunctionalTest, wait_for

class ItemValidationTest(SuperListsFunctionalTest):
    """
    Test's that the input for list items is validated before they are added.
    """
    def test_cannot_add_empty_list_item(self):
        """
        Functional test that one can not enter an empty list item.
        """
        # Edith goes to the home page ad accidentally tries to submit an empty list item.
        # She hits Enter on the empty input box.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # tha list items cannot be blank
        wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        # She tries again with some text for the tem, which now works
        #self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy milk')
        wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        
        # Perversely, she now decided to submit a second blank list item.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She recieves a similar warning on the list page
        wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
