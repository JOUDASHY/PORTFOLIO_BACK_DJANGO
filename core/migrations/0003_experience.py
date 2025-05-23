# Generated by Django 5.1.4 on 2024-12-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('entreprise', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('stage', 'Stage'), ('professionnel', 'Professionnel')], max_length=20)),
                ('role', models.CharField(max_length=255)),
            ],
        ),
    ]
