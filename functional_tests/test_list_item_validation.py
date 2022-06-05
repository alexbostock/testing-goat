from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationtest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith accidentally submits an empty list item.
        self.browser.get(self.live_server_url)
        self.get_new_item_input().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the page.
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # She types some text and the error disappears.
        self.get_new_item_input().send_keys('Buy milk')
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # She can submit successfully.
        self.get_new_item_input().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # She decides to submit a second blank list item.
        self.get_new_item_input().send_keys(Keys.ENTER)

        # She receives a similar error from the browser.
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # She can correct it by filling some text in.
        self.get_new_item_input().send_keys('Make tea')
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid')
        )
        self.get_new_item_input().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith creates a list with one item.
        self.browser.get(self.live_server_url)
        self.add_list_item('Go fishing')

        # She accidentally tries to enter a duplicate item.
        self.get_new_item_input().send_keys('Go fishing')
        self.get_new_item_input().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for_assertion(lambda: self.assertEqual(
            self.get_error_element().text,
            'You\'ve already got this in your list'
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error.
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_new_item_input().send_keys('Banter too thick')
        self.get_new_item_input().send_keys(Keys.ENTER)

        self.wait_for_assertion(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # She starts typing to clear the error.
        self.get_new_item_input().send_keys('a')

        # The error message disappears
        self.wait_for_assertion(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
