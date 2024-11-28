from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('test-gemini/', views.test_gemini, name='test_gemini'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
