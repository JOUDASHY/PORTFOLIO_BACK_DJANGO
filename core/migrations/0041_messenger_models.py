# Generated migration for Messenger models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_update_premier_contact_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessengerConversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_user_id', models.CharField(db_index=True, help_text='Facebook PSID (Page-Scoped ID) of the user', max_length=255)),
                ('page_id', models.CharField(help_text='Facebook Page ID', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Messenger Conversation',
                'verbose_name_plural': 'Messenger Conversations',
                'ordering': ['-updated_at'],
                'unique_together': {('facebook_user_id', 'page_id')},
            },
        ),
        migrations.CreateModel(
            name='MessengerMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(help_text='Facebook message ID (mid) for deduplication', max_length=255, unique=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')], max_length=20)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.messengerconversation')),
            ],
            options={
                'verbose_name': 'Messenger Message',
                'verbose_name_plural': 'Messenger Messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='messengermessage',
            index=models.Index(fields=['message_id'], name='core_messen_message_idx'),
        ),
        migrations.AddIndex(
            model_name='messengermessage',
            index=models.Index(fields=['conversation', 'created_at'], name='core_messen_convers_idx'),
        ),
    ]
