from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

TEST_EMAIL = 'test@example.com'

User = get_user_model()

class AuthenticationTest(TestCase):
    def test_returns_none_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        existing_user = User.objects.create(email=TEST_EMAIL)
        token = Token.objects.create(email=TEST_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.first()
        self.assertEqual(user, new_user)

class GetUserTest(TestCase):
    def test_get_user_by_email(self):
        User.objects.create(email='someother@email.com')
        desired_user = User.objects.create(email=TEST_EMAIL)
        found_user = PasswordlessAuthenticationBackend().get_user(TEST_EMAIL)
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_given_email(self):
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('foo'))
