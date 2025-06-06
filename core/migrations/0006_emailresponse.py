# Generated by Django 5.1.4 on 2024-12-30 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='core.email')),
            ],
        ),
    ]
