from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="joboffer",
            name="apply_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="joboffer",
            name="direct_apply",
            field=models.BooleanField(default=True),
        ),
    ]
