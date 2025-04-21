from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
# from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Education
from .serializers import EducationSerializer
from rest_framework import viewsets
from .models import Projet, ImageProjet
from .serializers import ProjetSerializer    
from .models import Experience
from .serializers import ExperienceSerializer
from django.core.mail import send_mail
from .models import Email, EmailResponse
from .serializers import EmailSerializer, EmailResponseSerializer,PasswordResetRequestSerializer
# import cloudinary.uploader
from django.urls import reverse
from django.core.files.storage import default_storage

import os
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework import status
from django.template.loader import get_template
from weasyprint import HTML
from .serializers import HistoricMailSerializer
from .serializers import UserRegistrationSerializer
from .serializers import UserDetailSerializer

from .models import HistoricMail


from .models import Langue
from .serializers import LangueSerializer

from rest_framework.decorators import api_view


from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Competence
from .serializers import CompetenceSerializer
from .models import Projet, ImageProjet
from .serializers import ProjetSerializer, ImageProjetSerializer
from .models import Formation

from .models import Formation,Award
from .serializers import FormationSerializer,AwardSerializer
from django.db.models import Avg
from .models import Rating
from .serializers import RatingSerializer
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Visit
from django.http import HttpRequest
from django.db.models import Count
from .models import Visit
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Facebook
from .serializers import FacebookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class KeepAliveView(APIView):
    authentication_classes = []  # Désactive l'authentification
    permission_classes = []  # Désactive les permissions

    def get(self, request):
        return Response({"status": "alive"})

class FacebookList(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Autoriser uniquement les utilisateurs authentifiés pour GET
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]  # Autoriser uniquement les administrateurs authentifiés pour DELETE
        return [AllowAny()]  # Autoriser tout le monde pour POST

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
            facebook_user = Facebook.objects.get(pk=pk)  # Recherche l'utilisateur Facebook par son id
            facebook_user.delete()  # Suppression de l'utilisateur
            return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Facebook.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
def clear_all_notifications(request):
    """
    Supprime toutes les notifications pour l'utilisateur authentifié.
    """
    Notification.objects.filter(user=request.user).delete()
    return Response({"status": "success", "message": "All notifications cleared."})



@api_view(["POST"])
def mark_all_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({"status": "success", "message": "All notifications marked as read."})



class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Récupérer toutes les notifications d'un utilisateur.
        """
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        notifications_data = [
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]
        return Response(notifications_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Créer une notification.
        """
        user = request.user
        title = request.data.get('title')
        message = request.data.get('message')

        if not title or not message:
            return Response(
                {"error": "Le titre et le message sont obligatoires."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Notification.objects.create(user=user, title=title, message=message)
        return Response({"message": "Notification créée avec succès."}, status=status.HTTP_201_CREATED)

    def patch(self, request, notification_id):
        """
        Marquer une notification comme lue.
        """
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marquée comme lue."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)


class NotificationTriggerView(APIView):
    """
    Vue pour créer une notification lors d'un événement spécifique.
    """

    def post(self, request):
        """
        Notifier lorsqu'un projet est noté ou atteint 5 visites en une journée.
        """
        user = request.user
        event_type = request.data.get('event_type')  # 'rating' ou 'view'
        project_id = request.data.get('project_id')

        if event_type == 'rating':
            Notification.objects.create(
                user=user,
                title="Nouveau vote reçu",
                message=f"Un internaute a noté votre projet ID {project_id}."
            )
            return Response({"message": "Notification créée pour une nouvelle note."}, status=status.HTTP_201_CREATED)

        elif event_type == 'view':
            # Vérifier les visites des dernières 24 heures
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            visits_count = Visit.objects.filter(created_at__range=(yesterday, today)).count()

            if visits_count >= 5:
                Notification.objects.create(
                    user=user,
                    title="Vues atteintes",
                    message=f"Votre projet a reçu {visits_count} vues en une journée."
                )
                return Response({"message": "Notification créée pour les vues."}, status=status.HTTP_201_CREATED)

        return Response({"error": "Type d'événement non valide."}, status=status.HTTP_400_BAD_REQUEST)




class MonthlyVisitStats(APIView):
    def get(self, request):
        # Récupère le mois actuel
        today = timezone.now()
        current_month_start = today.replace(day=1)
        stats = []

        # Récupère les visites pour les 12 derniers mois
        for i in range(12):
            month_start = current_month_start - relativedelta(months=i)
            month_end = month_start + relativedelta(months=1)
            
            # Comptage des visites pour chaque mois
            visit_count = Visit.objects.filter(
                timestamp__gte=month_start, timestamp__lt=month_end
            ).count()

            stats.append({
                "month": month_start.strftime('%B %Y'),
                "count": visit_count
            })

        return Response(stats)
        
            
class RecordVisit(APIView):
    permission_classes = [AllowAny]  # Permet l'accès à tout le monde

    def post(self, request: HttpRequest):
        ip_address = request.META.get('REMOTE_ADDR', '')  # Récupère l'adresse IP
        Visit.objects.create(ip_address=ip_address)  # Enregistre la visite
        return Response({"message": "Visit recorded successfully"}, status=status.HTTP_201_CREATED)



class TotalVisits(APIView):
    def get(self, request):
        total_visits = Visit.objects.count()  # Nombre total de visites
        return Response({"total_visits": total_visits})



class NotificationView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        notification = serializer.save(user=self.request.user)

        # Envoi de la notification en temps réel via WebSocket
        channel_layer = get_channel_layer()
        group_name = f"notifications_{self.request.user.id}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": {
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": str(notification.created_at),
                },
            }
        )



class RatingView(APIView):
    def post(self, request):
        project_id = request.data.get('project_id')
        score = request.data.get('score')
        ip_address = self.get_client_ip(request)

        # Vérifier si l'IP a déjà voté pour ce projet
        if Rating.objects.filter(project_id=project_id, ip_address=ip_address).exists():
            return Response({
                "message": "Vous avez déjà noté ce projet.",
                "ip_address": ip_address
            }, status=status.HTTP_400_BAD_REQUEST)

        # Enregistrer la nouvelle note
        rating = Rating.objects.create(project_id=project_id, score=score, ip_address=ip_address)
        return Response({
            "message": "Merci pour votre note !",
            "score": rating.score,
            "ip_address": ip_address
        }, status=status.HTTP_201_CREATED)
    
    def get_permissions(self):
        if self.request.method == 'POST':  # Autoriser l'accès public uniquement pour GET
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, project_id):
        # Calculer la moyenne des notes pour un projet
        ratings = Rating.objects.filter(project_id=project_id)
        average_score = ratings.aggregate(Avg('score'))['score__avg']
        ratings_count = ratings.count()

        # Ajouter les détails des notes si nécessaire (score + IP)
        ratings_details = list(ratings.values('score', 'ip_address'))

        return Response({
            "project_id": project_id,
            "average_score": round(average_score or 0, 2),
            "ratings_count": ratings_count,
            "ratings_details": ratings_details
        })

    def get_client_ip(self, request):
        """Récupérer l'adresse IP du client."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class FormationViewSet(viewsets.ModelViewSet):
  
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour GET
            return [AllowAny()]
        return [IsAuthenticated()]


class AwardViewSet(viewsets.ModelViewSet):
  
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour POST
            return [AllowAny()]
        return [IsAuthenticated()]  

class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer

    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour GET
            return [AllowAny()]
        return [IsAuthenticated()]


class ImageProjetViewSet(viewsets.ModelViewSet):
    queryset = ImageProjet.objects.all()
    serializer_class = ImageProjetSerializer

    def destroy(self, request, pk=None):
        image_projet = ImageProjet.objects.filter(pk=pk).first()  # Évite l'exception si l'image n'existe pas

        if image_projet:
            if image_projet.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image_projet.image))
                if os.path.exists(image_path):
                    os.remove(image_path)  # Supprime le fichier image
            image_projet.delete()  # Supprime l'objet de la base de données

        return Response({"message": "Image supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer

    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour LIST
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtenez l'instance actuelle
        old_image = instance.image  # Stockez l'image actuelle
        new_image = request.data.get('image')  # Vérifiez la nouvelle image dans la requête

        # Effectuez la mise à jour de l'instance
        response = super().update(request, *args, **kwargs)

        # Si une nouvelle image est fournie et que l'ancienne existe, supprimez l'ancienne
        if new_image and old_image and old_image.name != new_image:
            if default_storage.exists(old_image.path):  # Vérifiez si le fichier existe
                os.remove(old_image.path)  # Supprimez le fichier physique

        return response

    def perform_destroy(self, instance):
        """
        Supprime l'objet et son image associée.
        """
        if instance.image:  # Vérifiez si l'objet a une image
            if default_storage.exists(instance.image.path):  # Vérifiez si le fichier existe
                os.remove(instance.image.path)  # Supprimez le fichier physique

        # Supprimer l'instance de la base de données
        instance.delete()



# --------------------si cloudinary STORAGE---------------

# class CompetenceViewSet(viewsets.ModelViewSet):
#     queryset = Competence.objects.all()
#     serializer_class = CompetenceSerializer

#     def get_permissions(self):
#         if self.action == 'list':  # Autoriser l'accès public uniquement pour LIST
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()  # Obtenez l'instance actuelle
#         old_image = instance.image  # Stockez l'image actuelle
#         new_image = request.data.get('image')  # Vérifiez la nouvelle image dans la requête

#         # Effectuez la mise à jour de l'instance
#         response = super().update(request, *args, **kwargs)

#         # Si une nouvelle image est fournie et que l'ancienne existe, supprimez l'ancienne
#         if new_image and old_image and old_image != new_image:
#             # Si tu utilises Cloudinary
#             if old_image:
#                 # Supprime l'ancienne image sur Cloudinary si elle existe
#                 if old_image.url:
#                     public_id = old_image.url.split('/')[-1].split('.')[0]
#                     cloudinary.uploader.destroy(public_id)

#         return response

#     def perform_destroy(self, instance):
#         """
#         Supprime l'objet et son image associée.
#         """
#         if instance.image:  # Vérifiez si l'objet a une image
#             # Si tu utilises Cloudinary pour l'image
#             if instance.image.url:
#                 public_id = instance.image.url.split('/')[-1].split('.')[0]
#                 cloudinary.uploader.destroy(public_id)  # Supprime l'image sur Cloudinary

#         # Supprimer l'instance de la base de données
#         instance.delete()



class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                # Décoder le token d'accès pour récupérer l'utilisateur
                decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

                # Vérifier la validité du token
                exp = datetime.utcfromtimestamp(decoded_token['exp'])
                if exp < datetime.utcnow():
                    return Response({"error": "Token expiré."}, status=status.HTTP_400_BAD_REQUEST)

                # Récupérer l'utilisateur à partir de l'ID
                user_id = decoded_token['user_id']
                user = User.objects.get(id=user_id)

                # Mettre à jour le mot de passe
                user.set_password(new_password)
                user.save()

                return Response({"message": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)

            except jwt.ExpiredSignatureError:
                return Response({"error": "Token expiré."}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response({"error": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]  # Autorise tous les utilisateurs à accéder à cette vue

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                # Générer un token JWT
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)

                # Lien de réinitialisation basé sur le front-end
                frontend_base_url = settings.FRONTEND_BASE_URL  # Assurez-vous que FRONTEND_BASE_URL est défini
                reset_url = f"{frontend_base_url}/password-reset/{token}?email={email}"

                # Envoyer l'email
                send_mail(
                    subject="Réinitialisation de votre mot de passe",
                    message=f"Utilisez ce lien pour réinitialiser votre mot de passe : {reset_url}",
                    from_email="noreply@example.com",
                    recipient_list=[email],
                )
                return Response({"message": "Email envoyé pour la réinitialisation."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Utilisateur introuvable avec cet email."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Serializer pour les utilisateurs
@api_view(['GET'])
def get_all_users(request):
    try:
        # Récupération de tous les utilisateurs
        users = User.objects.all()
        # Sérialisation des données avec profils inclus
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # En cas d'erreur, retourner un message
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LangueViewSet(viewsets.ModelViewSet):
    queryset = Langue.objects.all()
    serializer_class = LangueSerializer
    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour GET
            return [AllowAny()]
        return [IsAuthenticated()]


class HistoricMailListView(APIView):
    def get(self, request):
        # Trier les emails par date et heure, du plus récent au plus ancien
        emails = HistoricMail.objects.all().order_by('-date_envoi', '-heure_envoi')
        
        # Sérialiser les emails
        serializer = HistoricMailSerializer(emails, many=True)
        
        # Retourner les données sérialisées
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import get_template
from weasyprint import HTML
from .models import HistoricMail
from django.conf import settings

class SendEmailView(APIView):
    def post(self, request):
        # Récupération des données du formulaire
        nom_entreprise = request.data.get('nomEntreprise')
        email_entreprise = request.data.get('emailEntreprise')
        lieu_entreprise = request.data.get('lieuEntreprise')

        # Créer le contenu du message
        subject = "Demande de stage"
        message = f'''Cher(e) Monsieur/Madame le/la responsable {nom_entreprise},
Je me permets de vous contacter afin de postuler pour un stage au sein de votre entreprise {nom_entreprise} . Je suis actuellement étudiant 3 ème année de licence en Informatique à l'ENI, et je suis très intéressé par l'opportunité de rejoindre votre entreprise pour compléter ma formation pratique.

Je suis particulièrement attiré par le développement Web Django, devops et administration Système et réseaux, et je suis convaincu que ce stage me permettrait d'acquérir des compétences précieuses dans le domaine.Voilà ainsi de suite mon CV et ma lettre de motivation'''

        from_email = settings.EMAIL_HOST_USER
        to_mail = email_entreprise

        # Créer le PDF à partir du modèle HTML
        pdf_file = self.generate_pdf(nom_entreprise, email_entreprise, lieu_entreprise)

        # Créez l'email avec les pièces jointes
        email = EmailMessage(subject, message, from_email, [to_mail])
        email.attach("LM_Eddy_Nilsen.pdf", pdf_file, "application/pdf")
        email.attach_file("CV_Eddy_Nilsen.pdf")
        email.send()  # Envoyer l'email

        # Enregistrement dans HistoricMail
        HistoricMail.objects.create(
            nom_entreprise=nom_entreprise,
            email_entreprise=email_entreprise,
            lieu_entreprise=lieu_entreprise
        )

        return Response({"message": "Email envoyé avec succès"}, status=status.HTTP_200_OK)

    def generate_pdf(self, nom_entreprise, email_entreprise, lieu_entreprise):
        """
        Génère un PDF à partir d'un modèle HTML et renvoie le contenu PDF sous forme de bytes.
        """
        # Préparer les données du modèle
        context = {
            'nom_entreprise': nom_entreprise,
            'email_entreprise': email_entreprise,
            'lieu_entreprise': lieu_entreprise
        }

        # Charger le modèle HTML
        template = get_template('app/LM.html')
        html_content = template.render(context)

        # Utiliser WeasyPrint pour générer le PDF à partir du HTML
        pdf_file = HTML(string=html_content).write_pdf()

        return pdf_file







class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all().order_by('-date', 'heure')
    serializer_class = EmailSerializer

    def get_permissions(self):
        if self.action == 'create':  # Autoriser l'accès public uniquement pour POST
            return [AllowAny()]
        return [IsAuthenticated()]
        
    def create(self, request, *args, **kwargs):
        # Appel à la méthode create parente pour créer l'email
        response = super().create(request, *args, **kwargs)
        
        # Si l'email a été créé avec succès
        if response.status_code == status.HTTP_201_CREATED:
            # Récupérer l'adresse email du client
            client_email = request.data.get('email')
            print(f"Email client reçu: {client_email}")  # Log pour débogage
            
            # Envoyer un email de confirmation automatique
            if client_email:
                try:
                    send_mail(
                        subject="Confirmation de réception de votre message",
                        message="Merci d'avoir envoyé votre message. Nous allons vous répondre dans les plus brefs délais.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client_email],
                        fail_silently=False,  # Afficher les erreurs
                    )
                    print(f"Email de confirmation envoyé à {client_email}")  # Log pour débogage
                except Exception as e:
                    print(f"Erreur lors de l'envoi de l'email: {str(e)}")  # Log pour débogage
                    
        return response    
class EmailResponseViewSet(viewsets.ModelViewSet):
    queryset = EmailResponse.objects.all()
    serializer_class = EmailResponseSerializer

    def get_queryset(self):
        # Récupère l'email_id de l'URL
        email_id = self.kwargs.get('email_id')  
        if email_id:
            # Filtre les réponses par email_id
            return EmailResponse.objects.filter(email__id=email_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        # Récupère l'email_id de l'URL
        email_id = self.kwargs.get('email_id')
        if not email_id:
            return Response({'error': 'Email ID is required in the URL'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Vérifie si l'email existe
            email = Email.objects.get(id=email_id)
        except Email.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        # Ajoute l'email à la requête et sérialise les données
        data = request.data.copy()
        data['email'] = email.id  # Associe l'email_id aux données

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Envoi de l'email
        response_message = data.get('response')  # Récupère le message de la réponse
        send_mail(
            subject="Réponse à votre email",  # Sujet de l'email
            message=response_message,  # Contenu du message
            from_email="no-reply@votre-domaine.com",  # Adresse de l'expéditeur
            recipient_list=[email.email],  # Liste des destinataires
            fail_silently=False,  # Lève une exception en cas d'échec
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Récupérer ou créer le profil de l'utilisateur connecté
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Récupérer les informations de l'utilisateur
            user_data = {
                "username": request.user.username,  # Récupérer le username
                "email": request.user.email         # Récupérer l'email
            }

            # Sérialiser les données du profil
            profile_data = ProfileSerializer(profile).data

            # Fusionner les données du profil et de l'utilisateur
            response_data = {**user_data, **profile_data}

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Gestion des erreurs si le profil ou d'autres erreurs surviennent
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NilsenProfileView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        try:
            # Récupérer l'utilisateur avec id=1
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            raise NotFound("User with id=1 does not exist.")

        # Construire une réponse JSON
        data = {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "image": user.profile.image.url if hasattr(user, 'profile') and user.profile.image else None,
            "about": getattr(user.profile, 'about', 'No description available'),
            "date_of_birth": getattr(user.profile, 'date_of_birth', None),
            "link_facebook": getattr(user.profile, 'link_facebook', None),
            "link_github": getattr(user.profile, 'link_github', None),
            "link_linkedin": getattr(user.profile, 'link_linkedin', None),
            "phone_number": getattr(user.profile, 'phone_number', None),
            "address": getattr(user.profile, 'address', None),
        }
        return Response(data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Créer un profil associé ou récupérer l'existant
            Profile.objects.get_or_create(user=user)

            # Générer un token JWT pour l'utilisateur inscrit
            refresh = RefreshToken.for_user(user)
            return Response({
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'User registered successfully!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour la connexion
class LoginView(APIView):
    permission_classes = [AllowAny]  # Accessible sans authentification préalable

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            # Recherche de l'utilisateur par email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Authentification de l'utilisateur
        user = authenticate(username=user.username, password=password)

        if user is not None:
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                  
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Invalid email or password."
            }, status=status.HTTP_401_UNAUTHORIZED)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # Utilisateur actuellement authentifié

        # Récupérer les données envoyées par l'utilisateur
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Vérification que l'ancien mot de passe est correct
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification que le nouveau mot de passe et la confirmation correspondent
        if new_password != confirm_password:
            return Response({"error": "New password and confirm password do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Validation de la longueur et de la sécurité du nouveau mot de passe
        if len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le mot de passe
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Ici, aucune suppression réelle n'est nécessaire pour les tokens JWT.
            return Response({
                'status': 'success',
                'message': 'Successfully logged out.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Education.
    """
    queryset = Education.objects.all().order_by('-annee_fin')
    serializer_class = EducationSerializer

    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour LIST
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtenez l'instance actuelle
        old_image = instance.image  # Stockez l'image actuelle
        new_image = request.data.get('image')  # Vérifiez la nouvelle image dans la requête

        # Effectuez la mise à jour de l'instance
        response = super().update(request, *args, **kwargs)

        # Si une nouvelle image est fournie et que l'ancienne existe, supprimez l'ancienne
        if new_image and old_image and old_image.name != new_image:
            if default_storage.exists(old_image.path):  # Vérifiez si le fichier existe
                os.remove(old_image.path)  # Supprimez le fichier physique

        return response

    def perform_destroy(self, instance):
        """
        Supprime l'objet et son image associée.
        """
        if instance.image:  # Vérifiez si l'objet a une image
            if default_storage.exists(instance.image.path):  # Vérifiez si le fichier existe
                os.remove(instance.image.path)  # Supprimez le fichier physique

        # Supprimer l'instance de la base de données
        instance.delete()

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('-date_fin')
    serializer_class = ExperienceSerializer
    def get_permissions(self):
        if self.action == 'list':  # Autoriser l'accès public uniquement pour POST
            return [AllowAny()]
        return [IsAuthenticated()]  



class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = request.user.profile  # Accéder au profil lié à l'utilisateur connecté
            old_image_path = profile.image.path if profile.image else None  # Chemin de l'image actuelle
            
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # Supprimer l'ancienne image si une nouvelle est téléchargée
                new_image_path = profile.image.path if profile.image else None
                if old_image_path and old_image_path != new_image_path:
                    default_storage.delete(old_image_path)
                
                return Response({"message": "Profil mis à jour avec succès", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({"error": "Profil introuvable"}, status=status.HTTP_404_NOT_FOUND)
