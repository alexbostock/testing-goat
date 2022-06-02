from django.contrib import auth
from django.test import TestCase
from accounts.models import Token

TEST_EMAIL = 'test@example.com'

User = auth.get_user_model()

class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email=TEST_EMAIL)
        user.full_clean()   # Should not raise

    def test_email_is_primary_key(self):
        user = User(email=TEST_EMAIL)
        self.assertEqual(user.pk, TEST_EMAIL)

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email=TEST_EMAIL)
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)   # Should not raise

class TokenModelTest(TestCase):
    def test_links_email_with_unique_auto_generated_id(self):
        token1 = Token.objects.create(email=TEST_EMAIL)
        token2 = Token.objects.create(email=TEST_EMAIL)
        self.assertNotEqual(token1.uid, token2.uid)
