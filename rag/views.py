import os

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatHistory
from .serializers import ChatHistorySerializer

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

        services_path = os.path.join(base_dir, "rag", "services.py")
        groq_only = False
        try:
            with open(services_path, "r", encoding="utf-8") as f:
                content = f.read()
            groq_only = "chromadb" not in content
        except OSError:
            pass

        return Response(
            {
                "status": "ok",
                "mode": "groq-only" if groq_only else "legacy-chroma",
                "groq_configured": bool(getattr(settings, "GROQ_API_KEY", None)),
                "cv_exists": os.path.exists(chemin_cv),
                "api_exists": os.path.exists(chemin_api),
            }
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

        ChatHistory.objects.create(
            user=user,
            role="user",
            content=question,
        )

        try:
            reponse = get_rag_service().repondre(question)

            ChatHistory.objects.create(
                user=user,
                role="assistant",
                content=reponse,
            )

            return Response({"reponse": reponse})
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


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ChatHistory.objects.filter(user=request.user)
        serializer = ChatHistorySerializer(messages, many=True)
        return Response(serializer.data)

    def delete(self, request):
        deleted_count, _ = ChatHistory.objects.filter(user=request.user).delete()
        return Response(
            {"message": f"{deleted_count} message(s) supprimé(s)"},
            status=status.HTTP_200_OK,
        )
