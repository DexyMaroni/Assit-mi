from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import ToDoForm
from .models import Task
from .serializers import TaskSerializer
import logging
import time

# Configure logger
logger = logging.getLogger(__name__)

# Web View for To-Do Application
def todo_view(request):
    """
    Handles the rendering and form submission for the web-based to-do app.
    """
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task']
            Task.objects.create(name=task_name)  # Save task to database
            return redirect('todo')  # Avoid duplicate submissions on refresh
    else:
        form = ToDoForm()

    # Fetch all tasks from the database
    tasks = Task.objects.all()

    return render(request, 'todo_app/todo.html', {'form': form, 'tasks': tasks})


def delete_task(request, pk):
    """
    Deletes a specific task by primary key.
    """
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('todo')


def edit_task(request, pk):
    """
    Edits a specific task by primary key.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            task.name = form.cleaned_data['task']
            task.save()
            return redirect('todo')
    else:
        form = ToDoForm(initial={'task': task.name})

    return render(request, 'todo_app/edit_task.html', {'form': form, 'task': task})


def complete_task(request, pk):
    """
    Marks a task as complete by toggling its completion status.
    """
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('todo')

@api_view(['PUT', 'DELETE'])
def task_detail(request, pk):
    """
    Handles updating or deleting a specific task by primary key.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=204)

@api_view(['GET', 'POST'])
def task_list(request):
    """
    Handles the creation of tasks and retrieves a list of all tasks.
    """
    if request.method == 'GET':
        # Retrieve all tasks from the database
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)