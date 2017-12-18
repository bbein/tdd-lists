"""
Input validation tests for the Super Lists App.
"""
from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import SuperListsFunctionalTest

class ItemValidationTest(SuperListsFunctionalTest):
    """
    Test's that the input for list items is validated before they are added.
    """
    @skip
    def test_cannot_add_empty_list_item(self):
        """
        Functional test that one can not enter an empty list item.
        """
        # Edith goes to the home page ad accidentally tries to submit an empty list item.
        # She hits Enter on the empty input box.

        # The home page refreshes, and there is an error message saying
        # tha list items cannot be blank

        # She tries again with some text for the tem, which now works

        # Perversely, she now decided to submit a second blank list item.

        # She recieves a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('Finish him!')
