'''from django.http import JsonResponse
from .gemini_utils import generate_content
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now
from .models import EmailVerificationToken, OTPModel
from .forms import OTPVerificationForm, RegistrationForm



@csrf_exempt
def test_gemini(request):
    prompt = "Explain how AI works"
    result = generate_content(prompt)
    return JsonResponse({"result": result})

User = get_user_model()

def send_otp(user):
    """Send an OTP to the user's email."""
    otp_token = EmailVerificationToken.objects.create(user=user)
    otp_token.generate_otp()  # Generate the OTP
    send_mail(
        'Your OTP for Email Verification',
        f'Your OTP is: {otp_token.token}',
        settings.DEFAULT_FROM_EMAIL,  # Use the default from email or define in settings
        [user.email],
    )

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Send OTP to user's email after successful registration
            send_otp(user)
            messages.info(request, "Please check your email for the OTP to verify your account.")
            return render(request,'verify_otp.html')  # Redirect to OTP verification page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        email = request.session.get('email')  # Retrieve email from session

        if not email:
            messages.error(request, "No email found in session. Please register again.")
            return redirect('register')

        # Check if the user exists
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, "User with this email does not exist.")
            return redirect('register')

        # Check if the OTP exists and is valid
        try:
            otp_object = OTPModel.objects.get(user=user, token=otp_input, is_used=False)
            otp_object.is_used = True  # Mark OTP as used
            otp_object.save()

            user.is_verified_status = True  # Mark user as verified
            user.save()

            messages.success(request, "Email verified successfully! You can now log in.")
            return redirect('login')  # Redirect to login page
        except OTPModel.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return redirect('verify_otp')
    return render(request, 'verify_otp.html')


'''


from django.shortcuts import render, redirect
from .forms import NoteForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from .gemini_utils import generate_content
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import CustomUser


def summarize_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            # Summarize the note content using Gemini API
            summarized_content = generate_content(note.content)
            note.content = summarized_content
            note.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()

    return render(request, 'summarize_note.html', {'form': form})


# This will store OTPs temporarily for testing purposes
otp_storage = {}

def send_otp(email):
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_otp(user.email)  # Send OTP after successful registration
            messages.success(request, 'Please check your email for the OTP.')
            return redirect('verify_otp.html', user_id=user.id)  # Redirect to OTP verification page
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if otp_entered and otp_storage.get(user.email) == int(otp_entered):
            user.is_active = True
            user.save()
            login(request, user)
            del otp_storage[user.email]  # Clear OTP after successful verification
            messages.success(request, 'Your email has been verified. You are now logged in.')
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html', {'user': user})


