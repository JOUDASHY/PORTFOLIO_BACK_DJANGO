import os

from django.conf import settings
from django.utils.text import Truncator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatHistory, Conversation
from .serializers import (
    ChatHistorySerializer,
    ConversationListSerializer,
    ConversationSerializer,
)

_rag_service = None


def get_rag_service():
    global _rag_service
    if _rag_service is None:
        from .services import RAGService

        _rag_service = RAGService()
    return _rag_service


class RAGHealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        base_dir = settings.BASE_DIR
        chemin_cv = os.path.join(base_dir, "CV_Eddy_Nilsen.pdf")
        chemin_api = os.path.join(base_dir, "API_DOCUMENTATION.md")

        try:
            rag = get_rag_service()
            nb_chunks = len(rag.chunks)
            bm25_ok = rag.bm25 is not None
        except Exception:
            nb_chunks = 0
            bm25_ok = False

        return Response(
            {
                "status": "ok",
                "mode": "bm25-rag",
                "groq_configured": bool(getattr(settings, "GROQ_API_KEY", None)),
                "cv_exists": os.path.exists(chemin_cv),
                "api_exists": os.path.exists(chemin_api),
                "chunks_loaded": nb_chunks,
                "bm25_ready": bm25_ok,
            }
        )


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationListSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get("title", "Nouvelle conversation")
        conversation = Conversation.objects.create(user=request.user, title=title)
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )


class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id, user=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation introuvable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def delete(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id, user=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation introuvable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        conversation.delete()
        return Response(
            {"message": "Conversation supprimée"},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id, user=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation introuvable"},
                status=status.HTTP_404_NOT_FOUND,
            )

        title = request.data.get("title")
        if title:
            conversation.title = title
            conversation.save()
            return Response(ConversationSerializer(conversation).data)

        return Response(
            {"error": "Le champ 'title' est requis"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response(
                {"error": "Le champ 'question' est requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        conversation_id = request.data.get("conversation_id")

        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id, user=user
                )
            except Conversation.DoesNotExist:
                return Response(
                    {"error": "Conversation introuvable"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            title = Truncator(question).chars(80, ellipsis="...")
            conversation = Conversation.objects.create(user=user, title=title)

        ChatHistory.objects.create(
            user=user,
            conversation=conversation,
            role="user",
            content=question,
        )

        try:
            reponse = get_rag_service().repondre(
                question, user=user, conversation=conversation
            )

            ChatHistory.objects.create(
                user=user,
                conversation=conversation,
                role="assistant",
                content=reponse,
            )

            conversation.save()

            return Response(
                {
                    "reponse": reponse,
                    "conversation_id": conversation.id,
                }
            )
        except Exception as e:
            import traceback

            log_path = os.path.join(settings.BASE_DIR, "rag_error.log")
            try:
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(traceback.format_exc())
            except OSError:
                pass
            print("ERREUR RAG:", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
