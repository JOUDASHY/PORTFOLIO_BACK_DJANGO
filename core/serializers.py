from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import (
    CV,
    Award,
    Competence,
    Education,
    Email,
    EmailResponse,
    Experience,
    Facebook,
    Formation,
    GalleryCategory,
    GalleryImage,
    HistoricMail,
    ImageProjet,
    Langue,
    MessageTemplate,
    MyLogin,
    Notification,
    Profile,
    Projet,
    Prospect,
    ProspectAttachment,
    ProspectMessage,
    ProspectNote,
    ProspectRating,
    Rating,
)


class _AbsoluteMediaUrlMixin:
    def _absolute_media_url(self, file_field):
        if not file_field:
            return None
        url = getattr(file_field, "url", None)
        if not url:
            return None
        # If already absolute, return as-is
        if url.startswith("http://") or url.startswith("https://"):
            return url
        base = getattr(settings, "BASE_URL", "").rstrip("/")
        media_url = getattr(settings, "MEDIA_URL", "/media/")
        # If URL already starts with MEDIA_URL, just prepend BASE_URL
        # Django's file_field.url already returns URLs starting with MEDIA_URL (e.g., /media/...)
        if url.startswith(media_url):
            return f"{base}{url}"
        # Otherwise, construct the full URL
        return f"{base}{media_url.rstrip('/')}/{url.lstrip('/')}"


class FacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facebook
        fields = ["id", "email", "password", "date", "heure"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "title", "message", "is_read", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "project_id", "ip_address", "score", "created_at"]
        read_only_fields = [
            "id",
            "created_at",
        ]  # Ces champs sont générés automatiquement


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class CompetenceSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = self._absolute_media_url(instance.image)
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
        fields = "__all__"


class HistoricMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricMail
        fields = [
            "id",
            "nom_entreprise",
            "email_entreprise",
            "lieu_entreprise",
            "date_envoi",
            "heure_envoi",
        ]


class EmailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailResponse
        fields = ["id", "email", "date", "heure", "response"]


class EmailSerializer(serializers.ModelSerializer):
    responses = EmailResponseSerializer(
        many=True, read_only=True
    )  # Inclure les réponses associées

    class Meta:
        model = Email
        fields = ["id", "name", "email", "message", "date", "heure", "responses"]


class ImageProjetSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = ImageProjet
        fields = ["id", "projet", "image"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = self._absolute_media_url(instance.image)
        return data


class ProjetSerializer(serializers.ModelSerializer):
    related_images = ImageProjetSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Projet
        fields = [
            "id",
            "nom",
            "description",
            "techno",
            "githublink",
            "projetlink",
            "related_images",
            "average_score",
        ]

    def get_average_score(self, obj):

        # Calculer la moyenne des scores pour le projet via project_id
        average = Rating.objects.filter(project_id=obj.id).aggregate(Avg("score"))[
            "score__avg"
        ]
        return round(average, 2) if average is not None else None


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "date_debut",
            "date_fin",
            "entreprise",
            "type",
            "role",
            "description",
        ]


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        # Création de l'utilisateur avec un mot de passe haché
        user = User(username=validated_data["username"], email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "image",
            "about",
            "date_of_birth",
            "link_facebook",
            "link_linkedin",
            "link_github",
            "link_instagram",
            "phone_number",
            "address",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = self._absolute_media_url(instance.image)
        return data


class UserDetailSerializer(ModelSerializer):
    profile = ProfileSerializer()  # Inclut le profil dans la sérialisation

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]


class EducationSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"  # Inclut tous les champs du modèle

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = self._absolute_media_url(instance.image)
        return data


class MyLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLogin
        fields = ["id", "site", "link", "username", "password"]


class CVSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = CV
        fields = ["id", "file", "file_url", "uploaded_at", "is_active"]
        read_only_fields = ["id", "uploaded_at", "file_url"]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


# =====================================================
# PROSPECTING SERIALIZERS
# =====================================================


class MessageTemplateSerializer(serializers.ModelSerializer):
    usage_type_display = serializers.CharField(
        source="get_usage_type_display", read_only=True
    )
    stage_display = serializers.CharField(source="get_stage_display", read_only=True)

    class Meta:
        model = MessageTemplate
        fields = [
            "id",
            "name",
            "language",
            "stage",
            "stage_display",
            "usage_type",
            "usage_type_display",
            "subject",
            "body",
            "cover_letter_html",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProspectNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectNote
        fields = ["id", "prospect", "content", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProspectMessageSerializer(serializers.ModelSerializer):
    channel_display = serializers.CharField(
        source="get_channel_display", read_only=True
    )

    class Meta:
        model = ProspectMessage
        fields = [
            "id",
            "prospect",
            "template",
            "channel",
            "channel_display",
            "subject",
            "body",
            "include_cv",
            "attachment_files",
            "status",
            "sent_at",
            "created_at",
        ]
        read_only_fields = ["id", "sent_at", "created_at"]


class ProspectAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for prospect attachments"""

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProspectAttachment
        fields = ["id", "name", "file", "file_url", "content_type", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def get_file_url(self, obj):
        """Get absolute URL for the file"""
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class ProspectRatingSerializer(serializers.ModelSerializer):
    """Serializer for prospect 5-star ratings"""

    class Meta:
        model = ProspectRating
        fields = ["id", "prospect", "rating", "comment", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProspectSerializer(serializers.ModelSerializer):
    notes = ProspectNoteSerializer(many=True, read_only=True)
    messages = ProspectMessageSerializer(many=True, read_only=True)
    ratings = ProspectRatingSerializer(many=True, read_only=True)  # ✨ Added ratings
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    source_display = serializers.CharField(source="get_source_display", read_only=True)

    class Meta:
        model = Prospect
        fields = [
            "id",
            "company_name",
            "contact_name",
            "email",
            "phone",
            "whatsapp_phone",
            "facebook_url",  # ✨ ADDED: Multi-channel fields
            "address",
            "city",
            "google_maps_url",
            "website_url",
            "has_website",
            "has_facebook",
            "status",
            "status_display",
            "estimated_value",
            "source",
            "source_display",
            "notes",
            "messages",
            "ratings",
            "created_at",
            "updated_at",  # ✨ Added ratings
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProspectListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list view"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    notes_count = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Prospect
        fields = [
            "id",
            "company_name",
            "contact_name",
            "email",
            "phone",
            "whatsapp_phone",
            "facebook_url",  # ✨ ADDED: Multi-channel fields
            "status",
            "status_display",
            "estimated_value",
            "city",
            "notes_count",
            "messages_count",
            "created_at",
            "updated_at",
        ]

    def get_notes_count(self, obj):
        return obj.prospect_notes.count()

    def get_messages_count(self, obj):
        return obj.messages.count()


# =====================================================
# GALLERY SERIALIZERS
# =====================================================


class GalleryCategorySerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField()

    class Meta:
        model = GalleryCategory
        fields = ["id", "name", "description", "images_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_images_count(self, obj):
        return obj.images.count()


class GalleryImageSerializer(_AbsoluteMediaUrlMixin, serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    image_url = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            "id",
            "category",
            "category_name",
            "title",
            "description",
            "image",
            "image_url",
            "tags",
            "tags_list",
            "is_featured",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "image_url", "tags_list"]

    def get_image_url(self, obj):
        return self._absolute_media_url(obj.image)

    def get_tags_list(self, obj):
        """Retourne les tags sous forme de liste Python"""
        if not obj.tags:
            return []
        return [tag.strip() for tag in obj.tags.split(",") if tag.strip()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = self._absolute_media_url(instance.image)
        return data


class ProspectStatsSerializer(serializers.Serializer):
    """Serializer for dashboard stats"""

    total_prospects = serializers.IntegerField()
    new = serializers.IntegerField()
    contacted = serializers.IntegerField()
    interested = serializers.IntegerField()
    proposal_sent = serializers.IntegerField()
    negotiation = serializers.IntegerField()
    won = serializers.IntegerField()
    lost = serializers.IntegerField()
    conversion_rate = serializers.CharField()
    estimated_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    won_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_deal_value = serializers.DecimalField(max_digits=10, decimal_places=2)
