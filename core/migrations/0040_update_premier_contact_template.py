# -*- coding: utf-8 -*-
from django.db import migrations


def update_premier_contact_template(apps, schema_editor):
    MessageTemplate = apps.get_model('core', 'MessageTemplate')
    Projet = apps.get_model('core', 'Projet')

    # Récupérer quelques projets existants pour les mentionner
    projets = list(Projet.objects.all()[:3])
    projets_lines = ""
    if projets:
        for p in projets:
            link = p.projetlink or p.githublink or ""
            if link:
                projets_lines += f"\n   • {p.nom} ({p.techno}) → {link}"
            else:
                projets_lines += f"\n   • {p.nom} ({p.techno})"
    else:
        projets_lines = "\n   • Portfolio personnel (Django + React)\n   • Application de gestion (Django REST)\n   • Site vitrine responsive (React + Tailwind)"

    body_fr = f"""Bonjour {{contact_name}},

Je suis Eddy Nilsen, développeur web full-stack basé à Madagascar.
Je crée des sites internet modernes et performants pour les entreprises locales.

J'ai remarqué que {{company_name}} n'a pas encore de présence en ligne.
Un site web vous permettrait de toucher plus de clients, de présenter vos services 24h/24 et d'apparaître sur Google.

Voici quelques exemples de mes réalisations :{projets_lines}

Je serais ravi de vous montrer ce que je pourrais créer pour {{company_name}}.

Email    : alitsiryeddynilsen@gmail.com
WhatsApp : +261 34 XX XXX XX
Facebook : https://www.facebook.com/eddy.nilsen

N'hésitez pas à me contacter, je réponds rapidement.

Cordialement,
Eddy Nilsen — Développeur Web"""

    body_en = f"""Hello {{contact_name}},

My name is Eddy Nilsen, a full-stack web developer based in Madagascar.
I build modern, high-performance websites for local businesses.

I noticed that {{company_name}} doesn't have an online presence yet.
A website would help you reach more customers, showcase your services 24/7, and appear on Google.

Here are some examples of my work:{projets_lines}

I'd love to show you what I could create for {{company_name}}.

Email    : alitsiryeddynilsen@gmail.com
WhatsApp : +261 34 XX XXX XX
Facebook : https://www.facebook.com/eddy.nilsen

Feel free to reach out — I respond quickly.

Best regards,
Eddy Nilsen — Web Developer"""

    # Mise à jour FR
    MessageTemplate.objects.filter(
        name='Premier contact',
        language='fr',
        stage='initial',
        usage_type='prospecting'
    ).update(
        body=body_fr,
        subject='Création de site web pour {company_name} — Eddy Nilsen, Développeur Web'
    )

    # Mise à jour EN
    MessageTemplate.objects.filter(
        name='First Contact',
        language='en',
        stage='initial',
        usage_type='prospecting'
    ).update(
        body=body_en,
        subject='Website creation for {company_name} — Eddy Nilsen, Web Developer'
    )


def reverse_premier_contact_template(apps, schema_editor):
    MessageTemplate = apps.get_model('core', 'MessageTemplate')

    MessageTemplate.objects.filter(
        name='Premier contact', language='fr', stage='initial'
    ).update(
        body="""Bonjour {contact_name},\n\nJe suis développeur web et je crée des sites internet pour les entreprises locales.\n\nJ'ai remarqué que {company_name} n'a pas encore de site web.\nUn site pourrait permettre à vos clients de voir vos services, vos horaires et vous trouver facilement sur internet.\n\nSi vous voulez, je peux vous montrer un exemple de site que je pourrais créer pour vous.\n\nCordialement,""",
        subject="Création de site web pour {company_name}"
    )

    MessageTemplate.objects.filter(
        name='First Contact', language='en', stage='initial'
    ).update(
        body="""Hello {contact_name},\n\nI'm a web developer creating websites for local businesses.\n\nI noticed that {company_name} doesn't have a website yet.\nA website could help your customers see your services, hours, and find you easily online.\n\nIf you'd like, I can show you an example of a website I could create for you.\n\nBest regards,""",
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
