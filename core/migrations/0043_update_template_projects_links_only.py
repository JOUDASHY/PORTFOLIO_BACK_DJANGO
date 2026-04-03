# -*- coding: utf-8 -*-
from django.db import migrations


def update_template(apps, schema_editor):
    MessageTemplate = apps.get_model('core', 'MessageTemplate')

    body_fr = (
        "Bonjour {contact_name},\n\n"
        "Je suis Eddy Nilsen, developpeur web full-stack base a Madagascar.\n"
        "Je cree des sites internet modernes et performants pour les entreprises locales.\n\n"
        "J'ai remarque que {company_name} n'a pas encore de presence en ligne.\n"
        "Un site web vous permettrait de toucher plus de clients, de presenter vos services 24h/24 et d'apparaitre sur Google.\n\n"
        "Voici quelques exemples de mes realisations :\n"
        "{my_projects}\n\n"
        "Je serais ravi de vous montrer ce que je pourrais creer pour {company_name}.\n\n"
        "Email    : {my_email}\n"
        "WhatsApp : {my_whatsapp}\n"
        "Facebook : {my_facebook}\n\n"
        "N'hesitez pas a me contacter, je reponds rapidement.\n\n"
        "Cordialement,\n"
        "Eddy Nilsen - Developpeur Web"
    )

    body_en = (
        "Hello {contact_name},\n\n"
        "My name is Eddy Nilsen, a full-stack web developer based in Madagascar.\n"
        "I build modern, high-performance websites for local businesses.\n\n"
        "I noticed that {company_name} doesn't have an online presence yet.\n"
        "A website would help you reach more customers, showcase your services 24/7, and appear on Google.\n\n"
        "Here are some examples of my work:\n"
        "{my_projects}\n\n"
        "I'd love to show you what I could create for {company_name}.\n\n"
        "Email    : {my_email}\n"
        "WhatsApp : {my_whatsapp}\n"
        "Facebook : {my_facebook}\n\n"
        "Feel free to reach out - I respond quickly.\n\n"
        "Best regards,\n"
        "Eddy Nilsen - Web Developer"
    )

    MessageTemplate.objects.filter(
        name='Premier contact', language='fr', stage='initial', usage_type='prospecting'
    ).update(body=body_fr)

    MessageTemplate.objects.filter(
        name='First Contact', language='en', stage='initial', usage_type='prospecting'
    ).update(body=body_en)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_update_template_dynamic_vars'),
    ]

    operations = [
        migrations.RunPython(update_template, migrations.RunPython.noop),
    ]
