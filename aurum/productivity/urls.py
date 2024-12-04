from django.urls import path
from .views import  text_generation_view, generate_content_view

urlpatterns = [
    path("ai/generate-notes/",  text_generation_view, name="generate_notes"),
    path("ai/transcribe_audio/",  generate_content_view, name="transcribe_audio"),
]
