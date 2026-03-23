import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0035_prospectmessage_include_cv"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebAuthnCredential",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "credential_id",
                    models.TextField(
                        help_text="Credential ID encodé en base64url (généré par l'appareil)",
                    ),
                ),
                (
                    "credential_id_hash",
                    models.CharField(
                        max_length=64,
                        unique=True,
                        blank=True,
                        help_text="SHA-256 hex digest du credential_id — index UNIQUE MySQL-compatible",
                    ),
                ),
                (
                    "public_key",
                    models.TextField(
                        help_text="Clé publique COSE encodée en base64url",
                    ),
                ),
                (
                    "sign_count",
                    models.IntegerField(
                        default=0,
                        help_text="Compteur de signatures (protection anti-replay)",
                    ),
                ),
                (
                    "aaguid",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        help_text="AAGUID de l'authenticator (identifie le type d'appareil)",
                    ),
                ),
                (
                    "device_name",
                    models.CharField(
                        default="Face ID / Biometric",
                        max_length=255,
                        help_text="Nom lisible de l'appareil (ex: iPhone 15 Face ID)",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "last_used_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        help_text="Dernière utilisation pour se connecter",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="webauthn_credentials",
                        to="auth.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "WebAuthn Credential",
                "verbose_name_plural": "WebAuthn Credentials",
                "ordering": ["-created_at"],
            },
        ),
    ]
