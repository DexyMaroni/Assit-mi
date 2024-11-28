from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'profile_picture', 'password1', 'password2']


from .models import EmailVerificationToken

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='Enter OTP')