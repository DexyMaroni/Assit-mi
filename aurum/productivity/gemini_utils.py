import google.generativeai as genai
from django.conf import settings

def generate_text_from_prompt(prompt, max_tokens=200, temperature=0.7):
    """
    Generate text based on a prompt.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"