from django.shortcuts import render
from django.http import JsonResponse
from .llm_integration import GeminiChatbot  

bot = GeminiChatbot()

def index(request):
    return render(request, 'index.html')  # Make sure this HTML exists

def chat_api(request):
    if request.method == "POST":
        data = request.POST if request.POST else request.body
        try:
            import json
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            else:
                data = dict(data)
            query = data.get("query", "")
        except Exception:
            query = ""

        reply = bot.generate_response(query)
        return JsonResponse({"response": reply})
    else:
        return JsonResponse({"error": "POST request required"}, status=400)
