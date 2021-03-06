from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self) -> None:
        # Edith opens the website
        self.browser.get(self.live_server_url)

        # She notices the site is about to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_new_item_input()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        input_box = self.get_new_item_input()
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_separate_lists_at_different_urls(self):
        # Edith starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy peacock feathers')

        # Edith notices that her list has a unique URL
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists/.+')

        # Now Francis comes along to the site, in a separate browser session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page, and doesn't see Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # Francis starts a list
        self.add_list_item('Buy milk')

        # Francis gets a unique URL
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, '/lists/.+')
        self.assertNotEqual(edith_url, francis_url)

        # Again, Francis doesn't see Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
