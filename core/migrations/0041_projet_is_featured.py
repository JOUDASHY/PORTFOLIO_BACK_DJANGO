from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_update_premier_contact_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
