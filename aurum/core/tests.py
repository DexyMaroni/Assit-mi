from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import EmailOTP
from core.utils import generate_otp, is_otp_valid
from django.utils.timezone import now, timedelta

User = get_user_model()

class OTPFunctionalityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.email_otp = EmailOTP.objects.create(user=self.user, otp=generate_otp())

    def test_generate_otp(self):
        otp = generate_otp()
        self.assertTrue(100000 <= otp <= 999999)

    def test_otp_expiry(self):
        # OTP should be valid within 5 minutes
        self.assertTrue(is_otp_valid(self.email_otp))

        # Simulate expiration
        self.email_otp.created_at = now() - timedelta(minutes=6)
        self.assertFalse(is_otp_valid(self.email_otp))
