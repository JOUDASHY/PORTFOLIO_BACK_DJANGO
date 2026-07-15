import json
import os
import re

import pdfplumber
from django.conf import settings
from groq import Groq
from rank_bm25 import BM25Okapi


def _tokeniser(text):
    text = text.lower()
    text = re.sub(r"[^\w\sàâäéèêëïîôùûüÿçœæ]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def _decouper_chunks(texte, source, taille=400, chevauchement=80):
    mots = texte.split()
    chunks = []
    i = 0
    while i < len(mots):
        morceau = " ".join(mots[i : i + taille])
        if morceau.strip():
            chunks.append({"texte": morceau, "source": source})
        i += taille - chevauchement
    return chunks


def _detecter_donnees(question, user):
    question_lower = question.lower()
    donnees = []

    if not user:
        return donnees

    try:
        from core.models import (
            ClientHack,
            Competence,
            Education,
            Email,
            Experience,
            Formation,
            GalleryImage,
            HistoricMail,
            Langue,
            MessageTemplate,
            MyLogin,
            Notification,
            Prospect,
            Projet,
            Visit,
        )

        if any(m in question_lower for m in ["login", "identifiant", "mot de passe", "connexion", "site web"]):
            items = MyLogin.objects.all()
            if items.exists():
                liste = [
                    {"site": m.site, "link": m.link, "username": m.username, "password": m.password}
                    for m in items
                ]
                donnees.append(("LOGINS", liste))

        if any(m in question_lower for m in ["projet", "portfolio", "application"]):
            items = Projet.objects.all()
            if items.exists():
                liste = [
                    {
                        "nom": p.nom,
                        "description": p.description[:150],
                        "techno": p.techno,
                        "github": p.githublink or "",
                        "link": p.projetlink or "",
                        "featured": p.is_featured,
                    }
                    for p in items
                ]
                donnees.append(("PROJETS", liste))

        if any(m in question_lower for m in ["compétence", "competence", "skill", "technologie", "tech"]):
            items = Competence.objects.all().order_by("-niveau")
            if items.exists():
                liste = [
                    {"nom": c.name, "niveau": c.niveau, "categorie": c.categorie or ""}
                    for c in items
                ]
                donnees.append(("COMPETENCES", liste))

        if any(m in question_lower for m in ["expérience", "experience", "stage", "emploi", "travail"]):
            items = Experience.objects.all().order_by("-date_debut")
            if items.exists():
                liste = [
                    {"entreprise": e.entreprise, "role": e.role, "type": e.type, "debut": str(e.date_debut), "fin": str(e.date_fin)}
                    for e in items
                ]
                donnees.append(("EXPERIENCES", liste))

        if any(m in question_lower for m in ["formation", "école", "ecole", "diplome", "étude"]):
            items = Formation.objects.all().order_by("-debut")
            if items.exists():
                liste = [{"titre": f.titre, "formateur": f.formateur, "debut": str(f.debut), "fin": str(f.fin)} for f in items]
                donnees.append(("FORMATIONS", liste))

        if any(m in question_lower for m in ["éducation", "education", "scolaire"]):
            items = Education.objects.all().order_by("-annee_debut")
            if items.exists():
                liste = [{"ecole": e.nom_ecole, "parcours": e.nom_parcours, "debut": str(e.annee_debut), "fin": str(e.annee_fin)} for e in items]
                donnees.append(("EDUCATION", liste))

        if any(m in question_lower for m in ["langue", "language", "français", "anglais"]):
            items = Langue.objects.all()
            if items.exists():
                liste = [{"langue": l.titre, "niveau": l.niveau} for l in items]
                donnees.append(("LANGUES", liste))

        if any(m in question_lower for m in ["récompense", "recompense", "prix", "award"]):
            items = Formation.objects.all()
            if items.exists():
                liste = [{"titre": f.titre, "formateur": f.formateur} for f in items]
                donnees.append(("FORMATIONS", liste))

        if any(m in question_lower for m in ["prospect", "client", "vente", "pipeline", "affaire"]):
            items = Prospect.objects.all().order_by("-created_at")
            if items.exists():
                liste = [
                    {
                        "entreprise": p.company_name,
                        "contact": p.contact_name,
                        "email": p.email or "",
                        "status": p.status,
                        "ville": p.city or "",
                        "valeur": str(p.estimated_value) if p.estimated_value else "",
                    }
                    for p in items
                ]
                donnees.append(("PROSPECTS", liste))

        if any(m in question_lower for m in ["stat", "statistique", "conversion", "revenu", "chiffre"]):
            from django.db.models import Avg, Count, Sum

            stats = Prospect.objects.aggregate(
                total=Count("id"),
                won=Count("id", filter={"status": "won"}),
                lost=Count("id", filter={"status": "lost"}),
                revenue=Sum("estimated_value", filter={"status": "won"}),
            )
            total = stats["total"] or 0
            won = stats["won"] or 0
            donnees.append(("STATISTIQUES", {
                "total_prospects": total,
                "gagnes": won,
                "perdus": stats["lost"] or 0,
                "taux_conversion": f"{round(won/total*100, 1) if total else 0}%",
                "revenu_total": str(stats["revenue"] or 0),
            }))

        if any(m in question_lower for m in ["email", "mail", "message", "contact form"]):
            items = Email.objects.all().order_by("-date")[:10]
            if items.exists():
                liste = [{"nom": e.name, "email": e.email, "message": e.message[:100], "date": str(e.date)} for e in items]
                donnees.append(("EMAILS_RECUS", liste))

        if any(m in question_lower for m in ["mail envoyé", "email envoyé", "prospection mail", "historique mail", "entreprise mail"]):
            items = HistoricMail.objects.all().order_by("-date_envoi")[:10]
            if items.exists():
                liste = [{"entreprise": m.nom_entreprise, "email": m.email_entreprise, "lieu": m.lieu_entreprise, "date": str(m.date_envoi)} for m in items]
                donnees.append(("MAILS_ENVOYES", liste))

        if any(m in question_lower for m in ["template", "modèle", "modele", "message template"]):
            items = MessageTemplate.objects.all()
            if items.exists():
                liste = [{"nom": t.name, "langue": t.language, "usage": t.usage_type, "sujet": t.subject} for t in items]
                donnees.append(("TEMPLATES", liste))

        if any(m in question_lower for m in ["notification", "alerte"]):
            items = Notification.objects.filter(user=user).order_by("-created_at")[:10]
            if items.exists():
                liste = [{"titre": n.title, "message": n.message, "lu": n.is_read, "date": str(n.created_at)} for n in items]
                donnees.append(("NOTIFICATIONS", liste))

        if any(m in question_lower for m in ["galerie", "gallery", "image", "photo"]):
            items = GalleryImage.objects.all().order_by("order")[:20]
            if items.exists():
                liste = [{"titre": g.title or f"Image #{g.pk}", "categorie": g.category.name if g.category else "", "tags": g.tags or ""} for g in items]
                donnees.append(("GALERIE", liste))

        if any(m in question_lower for m in ["visite", "visit", "traffic"]):
            from django.utils import timezone
            today = timezone.now().date()
            total = Visit.objects.count()
            today_count = Visit.objects.filter(timestamp__date=today).count()
            donnees.append(("VISITES", {"total": total, "aujourd_hui": today_count}))

        if any(m in question_lower for m in ["hack", "phishing", "simulation"]):
            items = ClientHack.objects.all()
            if items.exists():
                liste = [{"nom": c.name, "email": c.email, "actif": c.is_active, "soumissions": c.submissions.count()} for c in items]
                donnees.append(("CLIENTS_HACK", liste))

    except Exception as e:
        print(f"Erreur détection données: {e}")

    return donnees


class RAGService:
    def __init__(self):
        api_key = getattr(settings, "GROQ_API_KEY", None)
        self.groq_client = Groq(api_key=api_key) if api_key else None
        self.chunks = self._charger_documents()
        self.bm25 = self._indexer()

    def _charger_documents(self):
        base_dir = settings.BASE_DIR

        chemin_cv = None
        try:
            from core.models import CV

            cv = CV.objects.filter(is_active=True).first()
            if cv and cv.file:
                chemin_cv = cv.file.path
        except Exception as e:
            print(f"Erreur accès CV dynamique: {e}")

        if not chemin_cv or not os.path.exists(chemin_cv):
            chemin_cv = os.path.join(base_dir, "CV_Eddy_Nilsen.pdf")

        chemin_api = os.path.join(base_dir, "API_DOCUMENTATION.md")
        tous_les_chunks = []

        if os.path.exists(chemin_cv):
            cv_texte = self._extraire_cv(chemin_cv)
            if cv_texte.strip():
                tous_les_chunks.extend(_decouper_chunks(cv_texte, "CV"))
        else:
            print(f"CV introuvable: {chemin_cv}")

        if os.path.exists(chemin_api):
            api_texte = self._extraire_doc_api(chemin_api)
            if api_texte.strip():
                tous_les_chunks.extend(_decouper_chunks(api_texte, "API"))
        else:
            print(f"Doc API introuvable: {chemin_api}")

        print(f"RAG: {len(tous_les_chunks)} chunks chargés")
        return tous_les_chunks

    def _extraire_cv(self, chemin_pdf):
        texte = ""
        try:
            with pdfplumber.open(chemin_pdf) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        texte += page_text + "\n"
        except Exception as e:
            print(f"Erreur extraction CV: {e}")
        return texte

    def _extraire_doc_api(self, chemin_md):
        texte = ""
        try:
            with open(chemin_md, "r", encoding="utf-8") as f:
                if chemin_md.endswith(".md"):
                    texte = f.read()
                else:
                    spec = json.load(f)
                    for route, methodes in spec.get("paths", {}).items():
                        for methode, details in methodes.items():
                            texte += f"Route: {methode.upper()} {route}\n"
                            texte += f"Description: {details.get('summary', details.get('description', ''))}\n\n"
        except Exception as e:
            print(f"Erreur extraction API: {e}")
        return texte

    def _indexer(self):
        if not self.chunks:
            return None
        corpus_tokenise = [_tokeniser(c["texte"]) for c in self.chunks]
        return BM25Okapi(corpus_tokenise)

    def _rechercher(self, question, top_k=5):
        if not self.bm25 or not self.chunks:
            return []
        tokens_question = _tokeniser(question)
        scores = self.bm25.get_scores(tokens_question)
        indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        max_k = min(top_k, len(self.chunks))
        resultats = []
        for i in indices[:max_k]:
            if scores[i] > 0:
                resultats.append(self.chunks[i])
        return resultats

    def repondre(self, question, user=None, conversation=None):
        if not self.groq_client:
            return "Erreur: Clé API Groq non configurée sur le serveur."

        if not self.chunks:
            return "Erreur: Aucun document (CV/API) trouvé sur le serveur."

        morceaux = self._rechercher(question, top_k=5)

        if not morceaux:
            contexte = "\n\n".join(c["texte"] for c in self.chunks[:3])
        else:
            contexte = "\n\n".join(
                f"[{c['source']}]\n{c['texte']}" for c in morceaux
            )

        donnees = _detecter_donnees(question, user)
        if donnees:
            bloc_donnees = "\n\n".join(
                f"=== {titre} ===\n{json.dumps(donnees_brutes, ensure_ascii=False, default=str, indent=2)}"
                for titre, donnees_brutes in donnees
            )
            contexte += f"\n\n=== DONNÉES DE LA BASE DE DONNÉES ===\n{bloc_donnees}"

        historique = []
        if user:
            try:
                from .models import ChatHistory

                query = ChatHistory.objects.filter(user=user)
                if conversation:
                    query = query.filter(conversation=conversation)

                dernier_messages = query.order_by("-created_at")[:10]
                for msg in reversed(dernier_messages):
                    historique.append({"role": msg.role, "content": msg.content})
            except Exception as e:
                print(f"Erreur chargement historique: {e}")

        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es l'assistant personnel de l'auteur de ce CV et de cette API. "
                    "Tu as accès aux données réelles de la base de données ci-dessous. "
                    "Utilise ces données pour répondre directement à la question de l'utilisateur. "
                    "Affiche les données de manière claire et formatée. "
                    "Si aucune donnée n'est trouvée, dis-le honnêtement. "
                    "Réponds toujours en français.\n\n"
                    f"Contexte du CV/API:\n{contexte}"
                ),
            },
            *historique,
            {"role": "user", "content": question},
        ]

        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )
        return completion.choices[0].message.content
