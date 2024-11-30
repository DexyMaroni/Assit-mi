from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('summarize-note/', views.summarize_note, name='summarize_note'),
    path("register/", views.register, name="register"),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
]
