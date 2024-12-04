from django.shortcuts import render

# Create your views here.


# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .gemini_utils import generate_text_from_prompt
from .forms import TextGenerationForm

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



def generate_content_view(request):
    response = None

    if request.method == "POST":
        form = TextOrAudioGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            prompt = form.cleaned_data.get("prompt")
            audio_file = request.FILES.get("audio_file")
            max_tokens = form.cleaned_data["max_tokens"]
            temperature = form.cleaned_data["temperature"]

            if prompt:
                response = generate_text_from_prompt(prompt, max_tokens, temperature)
            elif audio_file:
                response = transcribe_audio(audio_file)

    else:
        form = TextOrAudioGenerationForm()

    return render(request, "content_generation.html", {"form": form, "response": response})