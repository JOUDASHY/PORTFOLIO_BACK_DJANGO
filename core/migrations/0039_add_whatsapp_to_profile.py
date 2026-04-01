from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_add_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='link_whatsapp',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
