from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Education

from .models import Experience

from .models import Projet, ImageProjet
from .models import Email, EmailResponse
from .models import HistoricMail
from .models import Langue
from django.contrib.auth.models import User
from .models import Competence
from .models import Award

from django.db.models import Avg


from .models import Formation


from rest_framework import serializers
from .models import Rating
from .models import Notification
from .models import Facebook
from .models import MyLogin
from django.conf import settings


class _AbsoluteMediaUrlMixin:
    def _absolute_media_url(self, file_field):
        if not file_field:
            return None
        url = getattr(file_field, 'url', None)
        if not url:
            return None
        # If already absolute, return as-is
        if url.startswith('http://') or url.startswith('https://'):
            return url
        base = getattr(settings, 'BASE_URL', '').rstrip('/')
        media_url = getattr(settings, 'MEDIA_URL', '/media/')
        # If URL already starts with MEDIA_URL, just prepend BASE_URL
        # Django's file_field.url already returns URLs starting with MEDIA_URL (e.g., /media/...)
        if url.startswith(media_url):
            return f"{base}{url}"
        # Otherwise, construct the full URL
        return f"{base}{media_url.rstrip('/')}/{url.lstrip('/')}"

class FacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facebook
        fields = ['id', 'email', 'password','date','heure']



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'project_id', 'ip_address', 'score', 'created_at']
        read_only_fields = ['id', 'created_at']  # Ces champs sont générés automatiquement




class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'



class CompetenceSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = self._absolute_media_url(instance.image)
        return data


        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email n'est pas enregistré.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_token(self, value):
        try:
            RefreshToken(value)  # Valider le token JWT
        except Exception:
            raise serializers.ValidationError("Token invalide ou expiré.")
        return value


class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = '__all__'



class HistoricMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricMail
        fields = ['id', 'nom_entreprise', 'email_entreprise', 'lieu_entreprise', 'date_envoi', 'heure_envoi']

class EmailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailResponse
        fields = ['id', 'email', 'date','heure','response']

class EmailSerializer(serializers.ModelSerializer):
    responses = EmailResponseSerializer(many=True, read_only=True)  # Inclure les réponses associées

    class Meta:
        model = Email
        fields = ['id', 'name', 'email', 'message','date','heure', 'responses']

        

class ImageProjetSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = ImageProjet
        fields = ['id', 'projet', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = self._absolute_media_url(instance.image)
        return data


class ProjetSerializer(serializers.ModelSerializer):
    related_images = ImageProjetSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Projet
        fields = ['id', 'nom', 'description', 'techno','githublink','projetlink', 'related_images', 'average_score']

    def get_average_score(self, obj):

        # Calculer la moyenne des scores pour le projet via project_id
        average = Rating.objects.filter(project_id=obj.id).aggregate(Avg('score'))['score__avg']
        return round(average, 2) if average is not None else None

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'date_debut', 'date_fin', 'entreprise', 'type', 'role', 'description']
class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        # Création de l'utilisateur avec un mot de passe haché
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'image', 'about', 'date_of_birth', 
            'link_facebook', 'link_linkedin', 'link_github',
            'phone_number', 'address'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = self._absolute_media_url(instance.image)
        return data


class UserDetailSerializer(ModelSerializer):
    profile = ProfileSerializer()  # Inclut le profil dans la sérialisation

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 
            'first_name', 'last_name', 'profile'
        ]




class EducationSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'  # Inclut tous les champs du modèle

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = self._absolute_media_url(instance.image)
        return data


class MyLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLogin
        fields = ['id', 'site', 'link', 'username', 'password']