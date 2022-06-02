from django.test import TestCase
from unittest.mock import call, patch
from accounts.models import Token
import superLists.settings as settings

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
        self.assertEqual(from_email, settings.EMAIL_HOST_USER)
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

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirects_to_home(self, mock_auth):
        response = self.client.post('/accounts/login?token=123456')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=123456')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='123456')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=123456')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        response = self.client.get('/accounts/login?token=123456')
        self.assertFalse(mock_auth.login.called)
