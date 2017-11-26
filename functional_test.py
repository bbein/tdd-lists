"""
Functional tests for the TDD Book Chapter 1 to ...
"""

import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    """
    Functional test for a new visitor to the website.
    """

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_txt):
        """
        checks if `row_text` is the text of one of the rows in the table
        """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_txt, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        """
        Functional test that we can start a list and retrive it later.
        """
        # Edith has heard about a cool new online to-do app. She goes
        # to check it out its hompage
        self.browser.get('http:\\localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box ( Edith's hoppy
        # is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table("1: Buy peacock feathers")
        # There is still a text box inviting her o add another item.
        # She enters "Use peacock feather to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Use peacock feather to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on her list.
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feather to make a fly")

        # Edith wonders whether the site will remember her list.
        # Then she notices that the site has generated a unique URL for her
        # -- there is some explanatory text to that effect.
        self.fail("Finish the test!")

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == "__main__":
    unittest.main(warnings='ignore')
