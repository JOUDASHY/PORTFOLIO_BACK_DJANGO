from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0047_clienthack_redirect_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="clienthack",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Si False, le lien ne fonctionne plus (suspendu)",
            ),
        ),
    ]
