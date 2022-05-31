from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token

TEST_EMAIL = 'test@example.com'

class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home(self):
        response = self.client.post('/accounts/send-login-email/', data={
            'email': TEST_EMAIL
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_email_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send-login-email/', data={
            'email': TEST_EMAIL
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Sign in to SuperLists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, [TEST_EMAIL])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send-login-email/', follow=True, data={
            'email': TEST_EMAIL
        })
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 'Check your email for your unique login link.')
        self.assertEqual(message.tags, 'success')

    def test_creates_token_for_email(self):
        self.client.post('/accounts/send-login-email/', data={
            'email': TEST_EMAIL
        })
        token = Token.objects.first()
        self.assertEqual(token.email, TEST_EMAIL)

    @patch('accounts.views.send_mail')
    def test_sends_link_with_token(self, mock_send_mail):
        self.client.post('/accounts/send-login-email/', data={
            'email': TEST_EMAIL
        })
        token = Token.objects.first()
        expected_url = f'/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

class LoginViewTest(TestCase):
    def test_redirects_to_home(self):
        response = self.client.post('/accounts/login?token=123456')
        self.assertRedirects(response, '/')
