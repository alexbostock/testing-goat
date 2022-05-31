from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import Token

TEST_EMAIL = 'test@example.com'

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email=TEST_EMAIL)
        user.full_clean()   # Should not raise

    def test_email_is_primary_key(self):
        user = User(email=TEST_EMAIL)
        self.assertEqual(user.pk, TEST_EMAIL)

class TokenModelTest(TestCase):
    def test_links_email_with_unique_auto_generated_id(self):
        token1 = Token.objects.create(email=TEST_EMAIL)
        token2 = Token.objects.create(email=TEST_EMAIL)
        self.assertNotEqual(token1.uid, token2.uid)
