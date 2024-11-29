from django.urls import path
from .views import test_gemini, sign_up, login_view

urlpatterns = [
    path('test_gemini/', test_gemini, name='test_gemini'),
    path('sign_up/', sign_up, name='sign_up'),
    path('login/', login_view, name='login'),
]
