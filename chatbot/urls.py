from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),             # Loads chatbot UI
    path('chat/', views.chat_api, name='chat_api'),  # API endpoint
]
