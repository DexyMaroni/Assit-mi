from django.urls import path
from .views import  text_generation_view
    

urlpatterns = [
    path("ai/generate-notes/",  text_generation_view, name="generate_notes"),
]
