from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("process_prompt/", views.process_prompt, name="process_prompt"),
    path("process_speech/", views.process_speech, name="process_speech"),
    path("text_to_speech/", views.text_to_speech, name="text_to_speech"),
    path("sorted_notes/", views.sorted_notes, name="sorted_notes"),
]

