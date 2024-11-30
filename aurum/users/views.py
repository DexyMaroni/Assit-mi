from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from .utils import generate_otp, send_otp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html', {'user': request.user})





