from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import speech
import google.generativeai as palm
from datetime import datetime
from .models import Transcription
import os

# Initialize Google PaLM with API key
palm.configure(api_key="AIzaSyBGyL4LKcHhi3AhxswV6FZt2u-ZZGKiue0")

# Initialize Google Speech-to-Text client
client = speech.SpeechClient()

def index(request):
    return render(request, "index.html")

def process_prompt(request):
    """
    Process a text prompt using Google PaLM.
    """
    if request.method == "POST":
        user_prompt = request.POST.get("prompt", "")

        try:
            # Generate response using PaLM
            response = palm.chat(
                model="models/chat-bison-001",  
                messages=[{"content": user_prompt}],
            )
            llm_message = response.get("candidates", [{}])[0].get("content", "Sorry, I couldn't generate a response.")
        except Exception as e:
            llm_message = f"Error: {str(e)}"

        return JsonResponse({"response": llm_message})

    return JsonResponse({"error": "Invalid request method."})

def process_speech(request):
    """
    Process speech recordings, transcribe them using Google Cloud Speech-to-Text,
    and organize transcriptions by date and time.
    """
    if request.method == "POST":
        # Get uploaded audio file
        audio_file = request.FILES.get("audio_file")
        if not audio_file:
            return JsonResponse({"error": "No audio file provided."})

        try:
            # Save the file temporarily
            temp_audio_path = "temp_audio.wav"
            with open(temp_audio_path, "wb") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Read audio file content
            with open(temp_audio_path, "rb") as audio_file_data:
                audio_content = audio_file_data.read()

            # Configure recognition settings
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,  # Update based on your file's sample rate
                language_code="en-US",
            )

            # Transcribe audio
            response = client.recognize(config=config, audio=audio)

            # Process transcriptions
            transcriptions = [
                {"text": result.alternatives[0].transcript, "confidence": result.alternatives[0].confidence}
                for result in response.results
            ]

            # Save each transcription to the database
            for transcription in transcriptions:
                Transcription.objects.create(
                    text=transcription["text"],
                    confidence=transcription["confidence"]
                )

            # Organize transcriptions by date and time
            sorted_transcriptions = Transcription.objects.all().order_by("-created_at")

            # Clean up temporary file
            os.remove(temp_audio_path)

            # Return the response
            return JsonResponse({
                "transcriptions": [{"text": t.text, "confidence": t.confidence, "created_at": t.created_at}
                                   for t in sorted_transcriptions]
            })
        except Exception as e:
            return JsonResponse({"error": f"Error processing speech: {str(e)}"})

    return JsonResponse({"error": "Invalid request method."})

