from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_view, name='todo'),
    path('api/tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('api/tasks/', views.task_list, name='task-list'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),
]