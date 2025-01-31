from django.db import migrations
from django.contrib.auth.models import User

def create_default_user(apps, schema_editor):
    # Vérifie si l'utilisateur existe déjà, sinon il est créé
    if not User.objects.filter(username='Nilsen').exists():
        User.objects.create_user(
            'Nilsen', 
            'alitsiryeddynilsen@gmail.com', 
            'lucienne98'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_projet_githublink_projet_projetlink'),
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]
