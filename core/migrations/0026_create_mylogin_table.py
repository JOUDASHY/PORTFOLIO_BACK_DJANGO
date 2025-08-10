from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0025_add_description_to_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=500)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Login',
                'verbose_name_plural': 'Logins',
            },
        ),
    ]
