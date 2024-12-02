from django.shortcuts import render, redirect
from .forms import ToDoForm

tasks = []  # Temporary in-memory storage for tasks

def todo_view(request):
    global tasks
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            tasks.append(task)  # Add task to the list
            return redirect('todo')  # Redirect to avoid re-posting form on refresh
    else:
        form = ToDoForm()
    
    return render(request, 'todo_app/todo.html', {'form': form, 'tasks': tasks})

