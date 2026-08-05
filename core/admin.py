from django.contrib import admin

from .models import (
    Award,
    Education,
    GalleryCategory,
    GalleryImage,
    MessageTemplate,
    Prospect,
    ProspectAttachment,
    ProspectMessage,
    ProspectNote,
    WebAuthnCredential,
)


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "usage_type",
        "language",
        "stage",
        "is_default",
        "created_at",
    ]
    list_filter = ["usage_type", "language", "stage", "is_default"]
    search_fields = ["name", "subject", "body"]

    fieldsets = (
        (
            "Informations",
            {"fields": ("name", "usage_type", "language", "stage", "is_default")},
        ),
        ("Contenu Email", {"fields": ("subject", "body")}),
        (
            "Lettre de Motivation (Stage uniquement)",
            {
                "fields": ("cover_letter_html",),
                "classes": ("collapse",),  # Section repliable
            },
        ),
    )


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "contact_name",
        "status",
        "estimated_value",
        "source",
        "created_at",
    ]
    list_filter = ["status", "source", "has_website", "has_facebook"]
    search_fields = ["company_name", "contact_name", "email", "city"]
    date_hierarchy = "created_at"


@admin.register(ProspectNote)
class ProspectNoteAdmin(admin.ModelAdmin):
    list_display = ["prospect", "created_at"]
    search_fields = ["prospect__company_name", "content"]


@admin.register(ProspectMessage)
class ProspectMessageAdmin(admin.ModelAdmin):
    list_display = [
        "prospect",
        "subject",
        "channel",
        "include_cv",
        "status",
        "sent_at",
        "created_at",
    ]
    list_filter = ["status", "channel", "include_cv"]
    search_fields = ["prospect__company_name", "subject"]


@admin.register(ProspectAttachment)
class ProspectAttachmentAdmin(admin.ModelAdmin):
    list_display = ["name", "uploaded_at", "content_type"]
    list_filter = ["uploaded_at"]
    search_fields = ["name"]


@admin.register(WebAuthnCredential)
class WebAuthnCredentialAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "device_name",
        "aaguid",
        "sign_count",
        "created_at",
        "last_used_at",
    ]
    list_filter = ["created_at", "last_used_at"]
    search_fields = ["user__username", "user__email", "device_name"]
    readonly_fields = [
        "credential_id",
        "public_key",
        "aaguid",
        "sign_count",
        "created_at",
        "last_used_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Utilisateur", {"fields": ("user", "device_name")}),
        (
            "Données cryptographiques (lecture seule)",
            {
                "fields": ("credential_id", "public_key", "aaguid", "sign_count"),
                "classes": ("collapse",),
                "description": "Ces données sont gérées automatiquement par le protocole WebAuthn.",
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at", "last_used_at"),
            },
        ),
    )


# =====================================================
# EDUCATION ADMIN
# =====================================================


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["nom_ecole", "nom_parcours", "annee_debut", "annee_fin", "lieu", "diplomes_count"]
    list_filter = ["annee_debut", "annee_fin"]
    search_fields = ["nom_ecole", "nom_parcours", "lieu"]
    
    def diplomes_count(self, obj):
        """Affiche le nombre de diplômes liés"""
        return obj.diplomes.count()
    
    diplomes_count.short_description = "Nb diplômes"


# =====================================================
# AWARD (DIPLOMES/CERTIFICATIONS) ADMIN
# =====================================================


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["titre", "education", "type", "institution", "annee"]
    list_filter = ["type", "annee"]
    search_fields = ["titre", "institution", "education__nom_ecole"]
    # autocomplete_fields = ["education"]  # Commenté temporairement
    fieldsets = (
        (
            "Informations du diplôme",
            {
                "fields": ("titre", "type", "institution", "annee"),
            },
        ),
        (
            "Parcours éducatif lié",
            {
                "fields": ("education",),
                "description": "Parcours éducatif ayant délivré ce diplôme/certification (optionnel)",
            },
        ),
    )


# =====================================================
# GALLERY ADMIN
# =====================================================


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "images_count", "created_at"]
    search_fields = ["name", "description"]

    def images_count(self, obj):
        return obj.images.count()

    images_count.short_description = "Nb images"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "category", "is_featured", "order", "created_at"]
    list_filter = ["category", "is_featured"]
    search_fields = ["title", "description", "tags"]
    list_editable = ["is_featured", "order"]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Contenu",
            {
                "fields": ("title", "description", "image", "tags"),
            },
        ),
        (
            "Organisation",
            {
                "fields": ("category", "is_featured", "order"),
            },
        ),
    )
