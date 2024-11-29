from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .gemini_utils import generate_content


@csrf_exempt
def test_gemini(request):
    prompt = "Explain how AI works"
    result = generate_content(prompt)
    return JsonResponse({"result": result})


@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            email = data.get("email", "")
            
            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            
            return JsonResponse({"message": "User created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == "GET":
        # Render the login page
        return render(request, 'login.html')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)