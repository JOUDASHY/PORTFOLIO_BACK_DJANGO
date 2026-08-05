# Generated manually for adding education ForeignKey to Award model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_messenger_models_manual'),
    ]

    operations = [
        # Ajouter le champ education (relation optionnelle vers Education)
        migrations.AddField(
            model_name='award',
            name='education',
            field=models.ForeignKey(
                blank=True,
                help_text='Parcours éducatif qui a délivré ce diplôme/certification',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='diplomes',
                to='core.education'
            ),
        ),
        
        # Modifier le champ type pour utiliser des choices
        migrations.AlterField(
            model_name='award',
            name='type',
            field=models.CharField(
                choices=[
                    ('diplome', 'Diplôme'),
                    ('certification', 'Certification'),
                    ('attestation', 'Attestation'),
                    ('brevet', 'Brevet'),
                    ('autre', 'Autre')
                ],
                default='diplome',
                help_text='Type de document obtenu',
                max_length=50
            ),
        ),
        
        # Ajouter help_text aux autres champs
        migrations.AlterField(
            model_name='award',
            name='titre',
            field=models.CharField(
                help_text='Ex: Master 2 Informatique, AWS Certified',
                max_length=255
            ),
        ),
        
        migrations.AlterField(
            model_name='award',
            name='institution',
            field=models.CharField(
                help_text='Organisme délivrant le diplôme',
                max_length=255
            ),
        ),
        
        migrations.AlterField(
            model_name='award',
            name='annee',
            field=models.IntegerField(help_text='Année d\'obtention'),
        ),
        
        # Mettre à jour les options du modèle
        migrations.AlterModelOptions(
            name='award',
            options={
                'ordering': ['-annee'],
                'verbose_name': 'Diplôme/Certification',
                'verbose_name_plural': 'Diplômes/Certifications'
            },
        ),
    ]
