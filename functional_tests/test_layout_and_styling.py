from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is centered
        input = self.get_new_item_input()
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list, and sees that the input box is centered there too
        input.send_keys('testing')
        input.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        input = self.get_new_item_input()
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=10
        )
