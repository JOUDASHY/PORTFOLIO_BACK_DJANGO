# -*- coding: utf-8 -*-
from django.db import migrations


def update_premier_contact_template(apps, schema_editor):
    MessageTemplate = apps.get_model('core', 'MessageTemplate')
    Projet = apps.get_model('core', 'Projet')

    # Projets marques is_featured en priorite, sinon les 3 premiers
    projets = list(Projet.objects.filter(is_featured=True)[:5])
    if not projets:
        projets = list(Projet.objects.all()[:3])

    projets_lines = ""
    if projets:
        for p in projets:
            link = p.projetlink or p.githublink or ""
            if link:
                projets_lines += "\n   - " + p.nom + " (" + p.techno + ") : " + link
            else:
                projets_lines += "\n   - " + p.nom + " (" + p.techno + ")"
    else:
        projets_lines = (
            "\n   - Portfolio personnel (Django + React)"
            "\n   - Application de gestion (Django REST)"
            "\n   - Site vitrine responsive (React + Tailwind)"
        )

    body_fr = (
        "Bonjour {contact_name},\n\n"
        "Je suis Eddy Nilsen, developpeur web full-stack base a Madagascar.\n"
        "Je cree des sites internet modernes et performants pour les entreprises locales.\n\n"
        "J'ai remarque que {company_name} n'a pas encore de presence en ligne.\n"
        "Un site web vous permettrait de toucher plus de clients, de presenter vos services 24h/24 et d'apparaitre sur Google.\n\n"
        "Voici quelques exemples de mes realisations :"
        + projets_lines +
        "\n\nJe serais ravi de vous montrer ce que je pourrais creer pour {company_name}.\n\n"
        "Email    : alitsiryeddynilsen@gmail.com\n"
        "WhatsApp : +261 34 XX XXX XX\n"
        "Facebook : https://www.facebook.com/eddy.nilsen\n\n"
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
        "Here are some examples of my work:"
        + projets_lines +
        "\n\nI'd love to show you what I could create for {company_name}.\n\n"
        "Email    : alitsiryeddynilsen@gmail.com\n"
        "WhatsApp : +261 34 XX XXX XX\n"
        "Facebook : https://www.facebook.com/eddy.nilsen\n\n"
        "Feel free to reach out - I respond quickly.\n\n"
        "Best regards,\n"
        "Eddy Nilsen - Web Developer"
    )

    MessageTemplate.objects.filter(
        name='Premier contact',
        language='fr',
        stage='initial',
        usage_type='prospecting'
    ).update(
        body=body_fr,
        subject='Creation de site web pour {company_name} - Eddy Nilsen, Developpeur Web'
    )

    MessageTemplate.objects.filter(
        name='First Contact',
        language='en',
        stage='initial',
        usage_type='prospecting'
    ).update(
        body=body_en,
        subject='Website creation for {company_name} - Eddy Nilsen, Web Developer'
    )


def reverse_premier_contact_template(apps, schema_editor):
    MessageTemplate = apps.get_model('core', 'MessageTemplate')

    MessageTemplate.objects.filter(
        name='Premier contact', language='fr', stage='initial'
    ).update(
        body="Bonjour {contact_name},\n\nJe suis developpeur web et je cree des sites internet pour les entreprises locales.\n\nJ'ai remarque que {company_name} n'a pas encore de site web.\n\nCordialement,",
        subject="Creation de site web pour {company_name}"
    )

    MessageTemplate.objects.filter(
        name='First Contact', language='en', stage='initial'
    ).update(
        body="Hello {contact_name},\n\nI'm a web developer creating websites for local businesses.\n\nI noticed that {company_name} doesn't have a website yet.\n\nBest regards,",
        subject="Website creation for {company_name}"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_add_whatsapp_to_profile'),
    ]

    operations = [
        migrations.RunPython(
            update_premier_contact_template,
            reverse_premier_contact_template
        ),
    ]
