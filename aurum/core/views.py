from django.http import JsonResponse
from .gemini_utils import generate_content
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def test_gemini(request):
    prompt = "Explain how AI works"
    result = generate_content(prompt)
    return JsonResponse({"result": result})


