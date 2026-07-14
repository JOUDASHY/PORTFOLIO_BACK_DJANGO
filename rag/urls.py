from django.urls import path

from .views import ChatHistoryView, ChatView, RAGHealthView

urlpatterns = [
    path("health/", RAGHealthView.as_view(), name="rag-health"),
    path("chat/", ChatView.as_view(), name="chat"),
    path("history/", ChatHistoryView.as_view(), name="chat-history"),
]
