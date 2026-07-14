from django.urls import path

from .views import (
    ChatView,
    ConversationDetailView,
    ConversationListView,
    RAGHealthView,
)

urlpatterns = [
    path("health/", RAGHealthView.as_view(), name="rag-health"),
    path("chat/", ChatView.as_view(), name="chat"),
    path(
        "conversations/",
        ConversationListView.as_view(),
        name="conversation-list",
    ),
    path(
        "conversations/<int:conversation_id>/",
        ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
]
