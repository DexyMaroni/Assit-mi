from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from .utils import generate_otp, send_otp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import random
from django.utils.timezone import now




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Temporarily deactivate user until OTP is verified
            otp = generate_otp()
            request.session['registration_data'] = {
                'email': user.email,
                'password': form.cleaned_data['password'],
                'first_name': user.first_name,
                'last_name': user.last_name,
                'otp': otp,
            }
            send_otp(user.email, otp)
            messages.success(request, "An OTP has been sent to your email.")
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})




def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(email=request.session.get('email'))
            if not user.is_active:
                if user.is_otp_valid():
                    if user.otp == otp:
                        user.is_active = True
                        user.otp = None
                        user.otp_created_at = None  # Clear timestamp
                        user.save()
                        login(request, user)
                        messages.success(request, "Your account has been verified and you're now logged in.")
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Invalid OTP. Please try again.")
                else:
                    messages.error(request, "OTP has expired. Please request a new one.")
                    return redirect('resend_otp')  # Add a route to resend OTP

            else:
                messages.warning(request, "Your account is already verified. Please log in.")
                return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, "User not found. Please register again.")
            return redirect('register')
    return render(request, 'users/otp_verification.html')



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        registration_data = request.session.get('registration_data')
        if registration_data and int(otp) == registration_data['otp']:
            user = CustomUser.objects.create_user(
                email=registration_data['email'],
                password=registration_data['password'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name']
            )
            user.is_active = True  # Activate the user after successful OTP verification
            user.save()
            messages.success(request, "Your account has been created successfully!")
            del request.session['registration_data']  # Clear session data
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'users/verify_otp.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are now logged in.")
                    return redirect('dashboard')  # Replace with your post-login page
                else:
                    messages.error(request, "Your account is inactive. Please contact support.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})





def resend_otp(request):
    try:
        user = CustomUser.objects.get(email=request.session.get('email'))
        if not user.is_active:
            user.otp = f"{random.randint(100000, 999999)}"
            user.otp_created_at = now()
            user.save()
            # Send the OTP via email (reuse your email-sending logic)
            send_otp(user.email, user.otp)
            messages.success(request, "A new OTP has been sent to your email.")
        else:
            messages.warning(request, "Your account is already verified. Please log in.")
            return redirect('login')
    except ObjectDoesNotExist:
        messages.error(request, "User not found. Please register again.")
        return redirect('register')
    return redirect('otp_verification')




def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page


@login_required
def dashboard(request):
    # Custom data based on the user
    user_data = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "role": request.user.groups.first().name if request.user.groups.exists() else "Student",
    }
    return render(request, "users/dashboard.html", {"user_data": user_data})




