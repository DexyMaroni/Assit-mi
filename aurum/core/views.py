from django.http import JsonResponse
from .gemini_utils import generate_content
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
import random



@csrf_exempt
def test_gemini(request):
    prompt = "Explain how AI works"
    result = generate_content(prompt)
    return JsonResponse({"result": result})


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now
from .models import EmailVerificationToken, OTPModel
from .forms import OTPVerificationForm, RegistrationForm
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
    if request.method == "POST":
        otp_input = request.POST.get("otp")  # Get OTP entered by the user
        user = request.user  # Assuming the user is logged in or passed via session
        
        try:
            # Retrieve the most recent unused OTP for the user
            otp_object = OTPModel.objects.get(user=user, token=otp_input, is_used=False)

            # Check if the OTP is expired
            expiration_time = otp_object.created_at + timedelta(minutes=10)  # Adjust as needed
            if now() > expiration_time:
                messages.error(request, "The OTP has expired. Please request a new one.")
                return redirect("verify_otp")

            # Mark OTP as used and activate the user
            otp_object.is_used = True
            otp_object.save()

            # Activate the user or perform other actions
            user.is_verified_status = True
            user.save()

            messages.success(request, "Your email has been verified successfully!")
            return redirect("dashboard")  # Redirect to the dashboard or another page

        except OTPModel.DoesNotExist:
            # OTP not found or already used
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

    # Render the OTP verification page
    return render(request, "verify_otp.html")

