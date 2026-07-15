import json

from core.models import (
    Award,
    ClientHack,
    Competence,
    DataHacked,
    Education,
    Email,
    Experience,
    Formation,
    GalleryCategory,
    GalleryImage,
    HistoricMail,
    Langue,
    MessageTemplate,
    MyLogin,
    Notification,
    Prospect,
    ProspectMessage,
    ProspectNote,
    ProspectRating,
    Projet,
    Profile,
    Visit,
)


def get_profile(user=None):
    if not user:
        return {"error": "Authentification requise"}
    try:
        profile = Profile.objects.get(user=user)
        return {
            "about": profile.about or "",
            "phone": profile.phone_number or "",
            "address": profile.address or "",
            "facebook": profile.link_facebook or "",
            "linkedin": profile.link_linkedin or "",
            "github": profile.link_github or "",
        }
    except Profile.DoesNotExist:
        return {"about": "", "phone": "", "address": ""}


def get_education(user=None):
    items = Education.objects.all().order_by("-annee_debut")
    return [
        {
            "ecole": e.nom_ecole,
            "parcours": e.nom_parcours,
            "debut": str(e.annee_debut),
            "fin": str(e.annee_fin),
            "lieu": e.lieu,
        }
        for e in items
    ]


def get_experiences(user=None, type_filter=None):
    qs = Experience.objects.all().order_by("-date_debut")
    if type_filter:
        qs = qs.filter(type=type_filter)
    return [
        {
            "entreprise": e.entreprise,
            "role": e.role,
            "type": e.type,
            "debut": str(e.date_debut),
            "fin": str(e.date_fin),
            "description": e.description or "",
        }
        for e in qs
    ]


def get_projects(user=None, featured_only=False):
    qs = Projet.objects.all().order_by("-id")
    if featured_only:
        qs = qs.filter(is_featured=True)
    return [
        {
            "nom": p.nom,
            "description": p.description,
            "techno": p.techno,
            "github": p.githublink or "",
            "link": p.projetlink or "",
            "featured": p.is_featured,
        }
        for p in qs
    ]


def get_competences(user=None, category=None, min_niveau=None):
    qs = Competence.objects.all().order_by("-niveau")
    if category:
        qs = qs.filter(categorie__icontains=category)
    if min_niveau:
        qs = qs.filter(niveau__gte=min_niveau)
    return [
        {
            "nom": c.name,
            "description": c.description,
            "niveau": c.niveau,
            "categorie": c.categorie or "",
        }
        for c in qs
    ]


def get_languages(user=None):
    items = Langue.objects.all()
    return [{"langue": l.titre, "niveau": l.niveau} for l in items]


def get_formations(user=None):
    items = Formation.objects.all().order_by("-debut")
    return [
        {
            "titre": f.titre,
            "formateur": f.formateur,
            "description": f.description,
            "debut": str(f.debut),
            "fin": str(f.fin),
        }
        for f in items
    ]


def get_awards(user=None):
    items = Award.objects.all().order_by("-annee")
    return [
        {
            "titre": a.titre,
            "institution": a.institution,
            "type": a.type,
            "annee": a.annee,
        }
        for a in items
    ]


def get_logins(user=None):
    if not user:
        return {"error": "Authentification requise"}
    items = MyLogin.objects.all().order_by("-id")
    return [
        {
            "site": m.site,
            "link": m.link,
            "username": m.username,
            "password": m.password,
        }
        for m in items
    ]


def get_prospects(user=None, status=None, city=None, limit=20):
    if not user:
        return {"error": "Authentification requise"}
    qs = Prospect.objects.all().order_by("-created_at")
    if status:
        qs = qs.filter(status=status)
    if city:
        qs = qs.filter(city__icontains=city)
    qs = qs[:limit]
    return [
        {
            "id": p.id,
            "entreprise": p.company_name,
            "contact": p.contact_name,
            "email": p.email or "",
            "telephone": p.phone or "",
            "ville": p.city or "",
            "status": p.status,
            "valeur": str(p.estimated_value) if p.estimated_value else "",
        }
        for p in qs
    ]


def get_prospect_stats(user=None):
    if not user:
        return {"error": "Authentification requise"}
    from django.db.models import Avg, Count, Sum

    stats = Prospect.objects.aggregate(
        total=Count("id"),
        won_count=Count("id", filter={"status": "won"}),
        lost_count=Count("id", filter={"status": "lost"}),
        won_revenue=Sum("estimated_value", filter={"status": "won"}),
        avg_value=Avg("estimated_value"),
    )
    total = stats["total"] or 0
    won = stats["won_count"] or 0
    conversion = round((won / total * 100), 1) if total > 0 else 0
    return {
        "total": total,
        "won": won,
        "lost": stats["lost_count"] or 0,
        "taux_conversion": f"{conversion}%",
        "revenue_gagne": str(stats["won_revenue"] or 0),
        "valeur_moyenne": str(round(stats["avg_value"] or 0, 2)),
    }


def get_received_emails(user=None, limit=10):
    if not user:
        return {"error": "Authentification requise"}
    items = Email.objects.all().order_by("-date")[:limit]
    return [
        {
            "nom": e.name,
            "email": e.email,
            "message": e.message[:200],
            "date": str(e.date),
        }
        for e in items
    ]


def get_sent_mail_history(user=None, limit=10):
    if not user:
        return {"error": "Authentification requise"}
    items = HistoricMail.objects.all().order_by("-date_envoi")[:limit]
    return [
        {
            "entreprise": m.nom_entreprise,
            "email": m.email_entreprise,
            "lieu": m.lieu_entreprise,
            "date": str(m.date_envoi),
        }
        for m in items
    ]


def get_hack_clients(user=None):
    if not user:
        return {"error": "Authentification requise"}
    items = ClientHack.objects.all()
    return [
        {
            "nom": c.name,
            "email": c.email,
            "token": c.token,
            "actif": c.is_active,
            "nb_soumissions": c.submissions.count(),
        }
        for c in items
    ]


def get_hack_data(user=None, client_id=None):
    if not user:
        return {"error": "Authentification requise"}
    qs = DataHacked.objects.all().order_by("-created_at")
    if client_id:
        qs = qs.filter(client_id=client_id)
    return [
        {
            "client": d.client.name,
            "email": d.email,
            "type": d.type,
            "date": str(d.created_at),
        }
        for d in qs[:30]
    ]


def get_prospect_notes(user=None, prospect_id=None):
    if not user:
        return {"error": "Authentification requise"}
    qs = ProspectNote.objects.all().order_by("-created_at")
    if prospect_id:
        qs = qs.filter(prospect_id=prospect_id)
    return [
        {
            "prospect": n.prospect.company_name,
            "contenu": n.content,
            "date": str(n.created_at),
        }
        for n in qs[:30]
    ]


def get_prospect_messages(user=None, prospect_id=None):
    if not user:
        return {"error": "Authentification requise"}
    qs = ProspectMessage.objects.all().order_by("-created_at")
    if prospect_id:
        qs = qs.filter(prospect_id=prospect_id)
    return [
        {
            "prospect": m.prospect.company_name,
            "canal": m.channel,
            "sujet": m.subject,
            "statut": m.status,
            "envoye": str(m.sent_at) if m.sent_at else "",
        }
        for m in qs[:30]
    ]


def get_message_templates(user=None, usage_type=None, language=None):
    if not user:
        return {"error": "Authentification requise"}
    qs = MessageTemplate.objects.all()
    if usage_type:
        qs = qs.filter(usage_type=usage_type)
    if language:
        qs = qs.filter(language=language)
    return [
        {
            "nom": t.name,
            "langue": t.language,
            "etape": t.stage,
            "usage": t.usage_type,
            "sujet": t.subject,
            "corps": t.body[:200],
            "defaut": t.is_default,
        }
        for t in qs
    ]


def get_gallery(user=None, category=None):
    items = GalleryImage.objects.all().order_by("order", "-created_at")
    if category:
        items = items.filter(category__name__icontains=category)
    return [
        {
            "titre": g.title or f"Image #{g.pk}",
            "description": g.description or "",
            "categorie": g.category.name if g.category else "",
            "tags": g.tags or "",
            "featured": g.is_featured,
            "ordre": g.order,
        }
        for g in items[:30]
    ]


def get_gallery_categories(user=None):
    cats = GalleryCategory.objects.all()
    return [
        {
            "nom": c.name,
            "description": c.description or "",
            "nb_images": c.images.count(),
        }
        for c in cats
    ]


def get_notifications(user=None):
    if not user:
        return {"error": "Authentification requise"}
    items = Notification.objects.filter(user=user).order_by("-created_at")[:20]
    return [
        {
            "titre": n.title,
            "message": n.message,
            "lu": n.is_read,
            "date": str(n.created_at),
        }
        for n in items
    ]


def get_visit_stats(user=None):
    if not user:
        return {"error": "Authentification requise"}
    from django.db.models import Count
    from django.utils import timezone

    today = timezone.now().date()
    total = Visit.objects.count()
    today_count = Visit.objects.filter(timestamp__date=today).count()
    return {
        "total_visites": total,
        "aujourd_hui": today_count,
    }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_profile",
            "description": "Récupère le profil personnel (bio, téléphone, adresse, réseaux sociaux).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_education",
            "description": "Liste tout le parcours scolaire (écoles, diplômes, dates, lieux).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_experiences",
            "description": "Liste les expériences professionnelles et stages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "type_filter": {
                        "type": "string",
                        "enum": ["stage", "professionnel"],
                        "description": "Filtrer par type.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": "Liste les projets du portfolio avec descriptions et technologies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "featured_only": {
                        "type": "boolean",
                        "description": "Si true, retourne uniquement les projets mis en avant.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_competences",
            "description": "Liste les compétences techniques avec niveau et catégorie.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filtrer par catégorie (ex: 'Frontend', 'Backend').",
                    },
                    "min_niveau": {
                        "type": "integer",
                        "description": "Niveau minimum (0-100).",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_languages",
            "description": "Liste les langues parlées et niveaux.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_formations",
            "description": "Liste les formations et cours suivis.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_awards",
            "description": "Liste les récompenses et prix obtenus.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_logins",
            "description": "Récupère tous les identifiants de connexion enregistrés (site, username, password).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prospects",
            "description": "Liste les prospects du pipeline commercial avec statut et coordonnées.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": [
                            "new",
                            "contacted",
                            "interested",
                            "proposal_sent",
                            "negotiation",
                            "won",
                            "lost",
                        ],
                        "description": "Filtrer par statut.",
                    },
                    "city": {
                        "type": "string",
                        "description": "Filtrer par ville.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Nombre max de résultats (défaut 20).",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prospect_stats",
            "description": "Statistiques du pipeline : total, taux de conversion, revenus.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_received_emails",
            "description": "Liste les emails reçus via le formulaire de contact.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Nombre max (défaut 10).",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_sent_mail_history",
            "description": "Liste les emails envoyés aux entreprises (historique de prospection).",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Nombre max (défaut 10).",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_hack_clients",
            "description": "Liste les clients de simulation de phishing avec leurs tokens et statuts.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_hack_data",
            "description": "Liste les données soumises par les victimes des campagnes de phishing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_id": {
                        "type": "integer",
                        "description": "Filtrer par ID client.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prospect_notes",
            "description": "Liste les notes et commentaires sur les prospects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prospect_id": {
                        "type": "integer",
                        "description": "Filtrer par ID prospect.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prospect_messages",
            "description": "Liste les messages envoyés aux prospects (email, WhatsApp, Facebook).",
            "parameters": {
                "type": "object",
                "properties": {
                    "prospect_id": {
                        "type": "integer",
                        "description": "Filtrer par ID prospect.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_message_templates",
            "description": "Liste les modèles de messages pour prospection ou demandes de stage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "usage_type": {
                        "type": "string",
                        "enum": ["prospecting", "internship"],
                        "description": "Filtrer par type d'utilisation.",
                    },
                    "language": {
                        "type": "string",
                        "enum": ["fr", "en"],
                        "description": "Filtrer par langue.",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_gallery",
            "description": "Liste les images de la galerie avec catégories et tags.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filtrer par nom de catégorie.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_gallery_categories",
            "description": "Liste les catégories de la galerie avec le nombre d'images.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_notifications",
            "description": "Liste les notifications de l'utilisateur.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_visit_stats",
            "description": "Statistiques de visites du portfolio (total et aujourd'hui).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_HANDLERS = {
    "get_profile": lambda user, **kw: get_profile(user),
    "get_education": lambda user, **kw: get_education(user),
    "get_experiences": lambda user, **kw: get_experiences(
        user, type_filter=kw.get("type_filter")
    ),
    "get_projects": lambda user, **kw: get_projects(
        user, featured_only=kw.get("featured_only", False)
    ),
    "get_competences": lambda user, **kw: get_competences(
        user, category=kw.get("category"), min_niveau=kw.get("min_niveau")
    ),
    "get_languages": lambda user, **kw: get_languages(user),
    "get_formations": lambda user, **kw: get_formations(user),
    "get_awards": lambda user, **kw: get_awards(user),
    "get_logins": lambda user, **kw: get_logins(user),
    "get_prospects": lambda user, **kw: get_prospects(
        user,
        status=kw.get("status"),
        city=kw.get("city"),
        limit=kw.get("limit", 20),
    ),
    "get_prospect_stats": lambda user, **kw: get_prospect_stats(user),
    "get_received_emails": lambda user, **kw: get_received_emails(
        user, limit=kw.get("limit", 10)
    ),
    "get_sent_mail_history": lambda user, **kw: get_sent_mail_history(
        user, limit=kw.get("limit", 10)
    ),
    "get_hack_clients": lambda user, **kw: get_hack_clients(user),
    "get_hack_data": lambda user, **kw: get_hack_data(
        user, client_id=kw.get("client_id")
    ),
    "get_prospect_notes": lambda user, **kw: get_prospect_notes(
        user, prospect_id=kw.get("prospect_id")
    ),
    "get_prospect_messages": lambda user, **kw: get_prospect_messages(
        user, prospect_id=kw.get("prospect_id")
    ),
    "get_message_templates": lambda user, **kw: get_message_templates(
        user, usage_type=kw.get("usage_type"), language=kw.get("language")
    ),
    "get_gallery": lambda user, **kw: get_gallery(
        user, category=kw.get("category")
    ),
    "get_gallery_categories": lambda user, **kw: get_gallery_categories(user),
    "get_notifications": lambda user, **kw: get_notifications(user),
    "get_visit_stats": lambda user, **kw: get_visit_stats(user),
}


def executer_tool(nom_tool, arguments, user):
    handler = TOOL_HANDLERS.get(nom_tool)
    if not handler:
        return {"error": f"Fonction inconnue: {nom_tool}"}
    try:
        return handler(user=user, **arguments)
    except Exception as e:
        return {"error": str(e)}
