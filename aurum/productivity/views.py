from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from .gemini_utils import generate_text_from_prompt
from .forms import TextGenerationForm
from .models import ToDo
from .forms import ToDoForm
from django.contrib.auth.decorators import login_required

def text_generation_view(request):
    if request.method == "POST":
        form = TextGenerationForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            max_tokens = form.cleaned_data['max_tokens']
            temperature = form.cleaned_data['temperature']

            # Call the utility function
            response = generate_text_from_prompt(prompt, max_tokens, temperature)

            return render(request, "text_generation.html", {
                "form": form,
                "response": response,
            })
    else:
        form = TextGenerationForm()

    return render(request, "text_generation.html", {"form": form})


@login_required
def todo_list(request):
    tasks = ToDo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todo_list')
    else:
        form = ToDoForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def toggle_task(request, task_id):
    task = ToDo.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('todo_list')

