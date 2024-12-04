from django.urls import path
from . import views
    

urlpatterns = [
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/add/', views.add_task, name='add_task'),
    path('todo/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path("ai/generate-notes/",  views.text_generation_view, name="generate_notes"),
]
