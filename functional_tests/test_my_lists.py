from django.contrib.auth import get_user_model
from .base import FunctionalTest
User = get_user_model()

TEST_EMAIL = 'alex@bostock.uk'

class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_mylists(self):
        # Edith is logged in.
        self.create_pre_authenticated_session(TEST_EMAIL)

        # She starts a list from the home page.
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # She notices and clicks a My Lists link.
        self.browser.find_element_by_link_text('My Lists').click()

        # She sees her list is there, labelled by its first item.
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for_assertion(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # She starts a second list.
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # She sees both lists under My Lists
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_link_text('My Lists').click()
        )
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for_assertion(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # She logs out. The My Lists option disappears.
        self.browser.find_element_by_link_text('Sign out').click()
        self.wait_for_assertion(
            lambda: self.assertEqual(self.browser.find_elements_by_link_text('My Lists'), [])
        )
