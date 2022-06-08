from selenium import webdriver
from .base import FunctionalTest

def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class SharingTest(FunctionalTest):
    def test_can_share_list_with_another_user(self):
        # Edith is authenticated.
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Her friend Fred is also using the app.
        fred_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(fred_browser))
        self.browser = fred_browser
        self.create_pre_authenticated_session('fred@example.com')

        # Edith starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # There is a Share button
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(share_box.get_attribute('placeholder'), 'friend@example.com')
