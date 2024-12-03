from django.shortcuts import render

# Create your views here.


# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .gemini_utils import generate_text_from_prompt

def text_generation_view(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        max_tokens = int(request.POST.get("max_tokens", 200))
        temperature = float(request.POST.get("temperature", 0.7))
        response = generate_text_from_prompt(prompt, max_tokens, temperature)
        return JsonResponse({"response": response})
    return render(request, "text_generation.html")

