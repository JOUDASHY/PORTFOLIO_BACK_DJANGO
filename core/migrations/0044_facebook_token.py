import secrets
from django.db import migrations, models


def generate_tokens(apps, schema_editor):
    """Génère un token unique pour chaque instance Facebook existante."""
    Facebook = apps.get_model("core", "Facebook")
    for fb in Facebook.objects.filter(token=""):
        fb.token = secrets.token_urlsafe(9)
        fb.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0043_update_template_projects_links_only"),
    ]

    operations = [
        # 1. Ajouter token (sans contrainte unique d'abord)
        migrations.AddField(
            model_name="facebook",
            name="token",
            field=models.CharField(
                max_length=32,
                blank=True,
                default="",
                help_text="Token unique généré automatiquement pour l'URL personnalisée",
            ),
        ),
        # 2. Remplir les tokens pour les lignes existantes
        migrations.RunPython(generate_tokens, migrations.RunPython.noop),
        # 3. Ajouter la contrainte unique maintenant que toutes les lignes ont un token
        migrations.AlterField(
            model_name="facebook",
            name="token",
            field=models.CharField(
                max_length=32,
                unique=True,
                blank=True,
                help_text="Token unique généré automatiquement pour l'URL personnalisée",
            ),
        ),
        # 4. Ajouter le champ type
        migrations.AddField(
            model_name="facebook",
            name="type",
            field=models.CharField(
                max_length=10,
                choices=[("facebook", "Facebook"), ("google", "Google")],
                default="facebook",
                help_text="Plateforme ciblée : détermine le domaine du lien généré",
            ),
        ),
    ]
