from selenium.webdriver.common.keys import Keys
from .base import wait

class MyListsPage():
    def __init__(self, test):
        self.test = test

    def go_to_my_lists_page(self):
        self.test.browser.find_button_by_link_text('My Lists').click()
        self.test.wait_for_assertion(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My Lists'
        ))
        return self
