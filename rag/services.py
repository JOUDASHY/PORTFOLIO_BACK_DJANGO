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
                    "Réponds UNIQUEMENT à partir du contexte ci-dessous. "
                    "Si l'information n'est pas dans le contexte, dis que tu ne sais pas.\n\n"
                    f"Contexte:\n{contexte}"
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
