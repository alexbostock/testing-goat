from selenium import webdriver

from functional_tests.test_my_lists import MyListsTest
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

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

        # Edith starts a list.
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # There is a Share button.
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'friend@example.com')

        # She shares her list. The page updates to say it is shared.
        list_page.share_list_with('fred@example.com')

        # Fred opens the My Lists page.
        self.browser = fred_browser
        list_page = MyListsPage(self).go_to_my_lists_page()

        # He sees Edith's list there.
        self.browser.find_button_by_link_text('Get help').click()

        # On the list page, Fred sees that the list belongs to Edith.
        self.browser.wait_for_assertion(
            list_page.get_list_owner(),
            'edith@example.com'
        )

        # He adds an item to the list
        list_page.add_list_item('Hi Edith')

        # When Edith refreshes the page, she sees Fred's item
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_list_item('Hi Edith', 2)
