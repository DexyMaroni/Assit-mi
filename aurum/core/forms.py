'''from django import forms
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
    otp = forms.CharField(max_length=6, required=True, label='Enter OTP')'''
    
    
    
from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category']

        

class OTPVerificationForm(forms.Form):
    otp = forms.IntegerField(label='Enter OTP')
    
    
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    middle_name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'middle_name', 'email', 'password1', 'password2')