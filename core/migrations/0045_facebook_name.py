from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0044_facebook_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="facebook",
            name="name",
            field=models.CharField(max_length=255, default=""),
        ),
    ]
