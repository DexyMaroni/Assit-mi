from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import random
from datetime import timedelta
from django.utils.timezone import now

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        default='profile_pictures/default.jpg'  # Default profile picture
    )
    is_verified_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.username}"

    def generate_otp(self):
        """Generates a random 6-digit OTP."""
        self.token = str(random.randint(100000, 999999))
        self.save()
        
        
class OTPModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)  # Expiry time of 10 minutes