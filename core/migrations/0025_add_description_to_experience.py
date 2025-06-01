from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0024_alter_competence_image'),  # Dépendance correcte basée sur votre historique
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
