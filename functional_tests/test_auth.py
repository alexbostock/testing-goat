from django.core import mail
import re
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

TEST_EMAIL = 'alex@bostock.uk'
SUBJECT = 'Sign in to SuperLists'

class AuthTest(FunctionalTest):
    def test_can_sign_in_with_email(self):
        # Edith navigates to the site and completes the sign in form.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears saying email sent.
        self.wait_for_assertion(lambda: self.assertIn(
            'Check your email for your unique login link.',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Edith receives an email.
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)

        # It contains a sign in link.
        self.assertIn('Use this link to sign in:', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find URL in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks the link.
        self.browser.get(url)

        # She is signed in.
        self.wait_for_assertion(
            lambda: self.browser.find_element_by_link_text('Sign out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # She signs out.
        self.browser.find_element_by_link_text('Sign out').click()

        # She is signed out.
        self.wait_for_assertion(lambda: self.browser.find_element_by_name('email'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)
