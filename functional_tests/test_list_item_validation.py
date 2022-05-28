from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationtest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith accidentally submits an empty list item.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message.
        self.wait_for_assertion(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'List item must not be empty'
            )
        )

        # She tries again with some text, which now works.
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # She decides to submit a second blank list item.
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page.
        self.wait_for_assertion(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                'List item must not be empty'
            )
        )

        # She can correct it by filling some text in.
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
