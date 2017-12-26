"""
Layout and styling tests for the Super Lists App.
"""
from selenium.webdriver.common.keys import Keys

from .base import SuperListsFunctionalTest

class LayoutAndStylingTest(SuperListsFunctionalTest):
    """
    Class to test the Layout and Styling of the Super Lists App
    """
    def test_layout_and_styling(self):
        """
        Functional test that our layout is loaded correctly.
        """
        # Edith goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10)

        # She satrts a new list and sees the inout is centered there too
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        inputbox = get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10)