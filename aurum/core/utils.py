import random
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from core.models import EmailOTP


def generate_otp():
    """Generates a 6-digit OTP."""
    return random.randint(100000, 999999)


def send_otp_email(email, otp):
    """
    Send an OTP to the specified email address.
    
    Args:
        email (str): Recipient's email address.
        otp (int): The OTP to send.
    """
    subject = "Your Verification OTP"
    message = f"Your OTP for email verification is: {otp}. This OTP is valid for 5 minutes."
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [email])
    
    
def is_otp_valid(email_otp_instance):
    """Checks if the OTP is still valid."""
    if email_otp_instance.created_at + timedelta(minutes=5) < now():
        return False
    return True


def send_verification_email(user):
    """
    Generate and send an OTP email to the user.
    """
    otp = generate_otp()

    # Save OTP to the database
    EmailOTP.objects.create(user=user, otp=otp)

    # Send the OTP to the user's email
    send_otp_email(user.email, otp)