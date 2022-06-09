from selenium.webdriver.common.keys import Keys
from .base import wait

class ListPage():
    def __init__(self, test):
        self.test = test

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_num):
        row_text = f'{item_num}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(row_text, [row.text for row in rows])

    def get_new_item_input(self):
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        num_rows = len(self.get_table_rows())
        self.get_new_item_input().send_keys(item_text)
        self.get_new_item_input().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(item_text, item_number)
        return self

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector('input[name="sharee"]')

    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector('.list-sharee')

    def share_list_with(self, sharee_email):
        self.get_share_box().sendKeys(sharee_email)
        self.get_share_box().sendKeys(Keys.ENTER)
        self.test.wait_for_assertion(lambda: self.test.assertIn(
            sharee_email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text
