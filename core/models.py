import hashlib
import ipaddress
import mimetypes

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)  # Titre de la notification
    message = models.TextField()  # Message de la notification
    is_read = models.BooleanField(default=False)  # Statut de lecture
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Formation(models.Model):
    titre = models.CharField(max_length=255)
    formateur = models.CharField(max_length=255)
    description = models.TextField()
    debut = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return self.titre


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    link_facebook = models.URLField(max_length=255, null=True, blank=True)
    link_linkedin = models.URLField(max_length=255, null=True, blank=True)
    link_github = models.URLField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def delete(self, *args, **kwargs):
        # Supprimer l'image si elle existe
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Education(models.Model):
    image = models.ImageField(upload_to="education_images/", blank=True, null=True)
    nom_ecole = models.CharField(max_length=255)
    nom_parcours = models.CharField(max_length=255)
    annee_debut = models.IntegerField()
    annee_fin = models.IntegerField()
    lieu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom_ecole} - {self.nom_parcours}"


class Experience(models.Model):
    TYPE_CHOICES = [
        ("stage", "Stage"),
        ("professionnel", "Professionnel"),
    ]
    date_debut = models.DateField()
    date_fin = models.DateField()
    entreprise = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    role = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.entreprise} - {self.role} ({self.type})"


class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    techno = models.CharField(max_length=100)
    githublink = models.URLField(blank=True, null=True)  # Lien GitHub (optionnel)
    projetlink = models.URLField(blank=True, null=True)  # Lien du projet (optionnel)

    def __str__(self):
        return self.nom


class Rating(models.Model):
    project_id = models.IntegerField()  # Identifiant du projet (ou portfolio)
    ip_address = models.GenericIPAddressField()  # Adresse IP du visiteur
    score = models.IntegerField()  # Note sur 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "project_id",
            "ip_address",
        )  # Empêche une même IP de voter plusieurs fois

    def __str__(self):
        return f"Project {self.project_id}, IP {self.ip_address}: {self.score}/5"


class ImageProjet(models.Model):
    projet = models.ForeignKey(
        Projet, related_name="related_images", on_delete=models.CASCADE
    )  # Nom unique
    image = models.ImageField(upload_to="projets/images/")

    def __str__(self):
        return f"Image de {self.projet.nom}"


class Email(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class EmailResponse(models.Model):
    email = models.ForeignKey(Email, related_name="responses", on_delete=models.CASCADE)
    response = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Response to {self.email.name}"


class Award(models.Model):
    titre = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    annee = models.IntegerField()

    def __str__(self):
        return self.titre


class HistoricMail(models.Model):
    nom_entreprise = models.CharField(max_length=255)
    email_entreprise = models.EmailField()
    lieu_entreprise = models.CharField(max_length=255)
    date_envoi = models.DateField(auto_now_add=True)  # Date automatique
    heure_envoi = models.TimeField(auto_now_add=True)  # Heure automatique

    def __str__(self):
        return f"{self.nom_entreprise} - {self.email_entreprise}"


class Langue(models.Model):
    titre = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return self.titre


# Valide que le fichier est un SVG
def validate_svg(file):
    mime_type, encoding = mimetypes.guess_type(file.name)
    if mime_type != "image/svg+xml":
        raise ValidationError("Le fichier doit être au format SVG.")


class Competence(models.Model):
    image = models.FileField(
        upload_to="competences/images/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["svg", "png", "jpg", "jpeg"])
        ],  # Autoriser plusieurs formats
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    niveau = models.IntegerField()
    categorie = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Visit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"Visit from {self.ip_address} at {self.timestamp}"


class Facebook(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Texte clair pour le mot de passe
    date = models.DateField(auto_now_add=True)  # Date automatique lors de la création
    heure = models.TimeField(auto_now_add=True)  # Heure automatique lors de la création

    def __str__(self):
        return self.email


class MyLogin(models.Model):
    site = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.site} - {self.username}"

    class Meta:
        verbose_name = "Login"
        verbose_name_plural = "Logins"


class CV(models.Model):
    """Model for storing CV PDF file"""

    file = models.FileField(
        upload_to="cv/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"CV - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"

    def save(self, *args, **kwargs):
        # Ensure only one active CV at a time
        if self.is_active:
            CV.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file when the model instance is deleted
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


# =====================================================
# PROSPECTING MODULE
# =====================================================


class MessageTemplate(models.Model):
    """Reusable message templates for prospecting AND internship requests"""

    LANGUAGE_CHOICES = [
        ("fr", "Français"),
        ("en", "English"),
    ]
    STAGE_CHOICES = [
        ("initial", "Initial Contact"),
        ("follow_up", "Follow Up"),
        ("proposal", "Proposal"),
        ("closing", "Closing"),
    ]
    USAGE_TYPE_CHOICES = [
        ("prospecting", "Prospecting (Sales)"),
        ("internship", "Internship Request"),
    ]

    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="fr")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="initial")
    usage_type = models.CharField(
        max_length=20, choices=USAGE_TYPE_CHOICES, default="prospecting"
    )
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    cover_letter_html = models.TextField(
        blank=True, help_text="HTML template for PDF generation (internship only)"
    )
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_usage_type_display()} - {self.language})"

    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"
        ordering = ["usage_type", "stage", "language", "name"]


class Prospect(models.Model):
    """Potential client for web development services"""

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("interested", "Interested"),
        ("proposal_sent", "Proposal Sent"),
        ("negotiation", "Negotiation"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]
    SOURCE_CHOICES = [
        ("google_maps", "Google Maps"),
        ("referral", "Referral"),
        ("social", "Social Media"),
        ("direct", "Direct Contact"),
        ("other", "Other"),
    ]

    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Numéro WhatsApp (avec indicatif, ex: +261...)",
    )
    facebook_url = models.URLField(blank=True, help_text="URL Page Facebook ou profil")
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    google_maps_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    has_website = models.BooleanField(default=False)
    has_facebook = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default="google_maps"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"
        ordering = ["-created_at"]


class ProspectNote(models.Model):
    """Notes and conversation history for a prospect"""

    prospect = models.ForeignKey(
        Prospect, on_delete=models.CASCADE, related_name="prospect_notes"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.prospect.company_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Prospect Note"
        verbose_name_plural = "Prospect Notes"
        ordering = ["-created_at"]


class ProspectMessage(models.Model):
    """Track messages sent to prospects"""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("opened", "Opened"),
        ("replied", "Replied"),
    ]
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("whatsapp", "WhatsApp"),
        ("facebook", "Facebook Messenger"),
    ]

    prospect = models.ForeignKey(
        Prospect, on_delete=models.CASCADE, related_name="messages"
    )
    template = models.ForeignKey(
        MessageTemplate, on_delete=models.SET_NULL, null=True, blank=True
    )
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="email")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    include_cv = models.BooleanField(
        default=False,
        help_text="Automatically attach CV from database (for email channel only)",
    )
    attachment_files = models.JSONField(
        null=True,
        blank=True,
        default=list,
        help_text="List of attached file URLs stored in media/ (for email channel only)",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message to {self.prospect.company_name} - {self.status}"

    class Meta:
        verbose_name = "Prospect Message"
        verbose_name_plural = "Prospect Messages"
        ordering = ["-created_at"]


class ProspectAttachment(models.Model):
    """File attachments for prospecting emails"""

    name = models.CharField(max_length=255)  # Original filename
    file = models.FileField(upload_to="prospect_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100, blank=True)  # MIME type

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Prospect Attachment"
        verbose_name_plural = "Prospect Attachments"
        ordering = ["-uploaded_at"]


class ProspectRating(models.Model):
    """5-star rating system for prospects (quality, interest level, etc.)"""

    prospect = models.ForeignKey(
        Prospect, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars",
    )
    comment = models.TextField(
        blank=True, help_text="Optional comment about this rating"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prospect.company_name} - {'⭐' * self.rating} ({self.rating}/5)"

    class Meta:
        verbose_name = "Prospect Rating"
        verbose_name_plural = "Prospect Ratings"
        ordering = ["-created_at"]
        unique_together = ["prospect"]  # One rating per prospect (can be updated)


# =====================================================
# WEBAUTHN / FACE ID MODULE
# =====================================================


class WebAuthnCredential(models.Model):
    """
    Stocke les clés publiques WebAuthn (Face ID, Touch ID, Windows Hello).
    La biométrie ne quitte JAMAIS l'appareil — seule la clé publique est conservée.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="webauthn_credentials"
    )
    # Identifiant unique du credential (base64url) généré par l'appareil
    # Stocké en TEXT — l'unicité est garantie par credential_id_hash (SHA-256)
    credential_id = models.TextField()
    # Hash SHA-256 du credential_id — index UNIQUE MySQL-compatible (VARCHAR 64)
    # Un digest SHA-256 fait toujours 64 caractères hexadécimaux → taille fixe
    credential_id_hash = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        help_text="SHA-256 hex digest du credential_id (auto-généré à la création)",
    )
    # Clé publique COSE encodée en base64url
    public_key = models.TextField()
    # Compteur de signatures — protection contre les attaques de rejeu
    sign_count = models.IntegerField(default=0)
    # AAGUID : identifie le modèle d'authenticator (ex: Touch ID, Face ID…)
    aaguid = models.CharField(max_length=255, blank=True)
    # Nom lisible donné par l'utilisateur (ex: "iPhone 15 Face ID")
    device_name = models.CharField(max_length=255, default="Face ID / Biometric")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Auto-génère credential_id_hash avant chaque sauvegarde."""
        if self.credential_id and not self.credential_id_hash:
            self.credential_id_hash = hashlib.sha256(
                self.credential_id.encode("utf-8")
            ).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.device_name}"

    class Meta:
        verbose_name = "WebAuthn Credential"
        verbose_name_plural = "WebAuthn Credentials"
        ordering = ["-created_at"]
