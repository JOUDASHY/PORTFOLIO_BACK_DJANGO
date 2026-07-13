from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import RAGService

# We initialize it outside to keep chroma and groq instances in memory across requests
rag_service = RAGService()

class ChatView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Le champ 'question' est requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reponse = rag_service.repondre(question)
            return Response({"reponse": reponse})
        except Exception as e:
            import traceback
            import os
            from django.conf import settings
            log_path = os.path.join(settings.BASE_DIR, "rag_error.log")
            try:
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(traceback.format_exc())
            except:
                pass
            print("ERREUR RAG:", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
