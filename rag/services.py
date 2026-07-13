import json
import os

import pdfplumber
from django.conf import settings
from groq import Groq


class RAGService:
    def __init__(self):
        api_key = getattr(settings, "GROQ_API_KEY", None)
        self.groq_client = Groq(api_key=api_key) if api_key else None
        self.contexte = self._charger_contexte()

    def _charger_contexte(self):
        base_dir = settings.BASE_DIR
        chemin_cv = os.path.join(base_dir, "CV_Eddy_Nilsen.pdf")
        chemin_api = os.path.join(base_dir, "API_DOCUMENTATION.md")

        parties = []

        if os.path.exists(chemin_cv):
            cv_texte = self.extraire_cv(chemin_cv)
            if cv_texte.strip():
                parties.append(f"=== CV ===\n{cv_texte}")
        else:
            print(f"Fichier introuvable: {chemin_cv}")

        if os.path.exists(chemin_api):
            api_texte = self.extraire_doc_api(chemin_api)
            if api_texte.strip():
                parties.append(f"=== DOCUMENTATION API ===\n{api_texte}")
        else:
            print(f"Fichier introuvable: {chemin_api}")

        return "\n\n".join(parties)

    def extraire_cv(self, chemin_pdf):
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

    def extraire_doc_api(self, chemin_md):
        texte = ""
        try:
            if chemin_md.endswith(".md"):
                with open(chemin_md, "r", encoding="utf-8") as f:
                    texte = f.read()
            else:
                with open(chemin_md, "r", encoding="utf-8") as f:
                    spec = json.load(f)
                for route, methodes in spec.get("paths", {}).items():
                    for methode, details in methodes.items():
                        texte += f"Route: {methode.upper()} {route}\n"
                        texte += f"Description: {details.get('summary', details.get('description', ''))}\n\n"
        except Exception as e:
            print(f"Erreur extraction API: {e}")
        return texte

    def repondre(self, question):
        if not self.groq_client:
            return "Erreur: Clé API Groq non configurée sur le serveur."

        if not self.contexte.strip():
            return "Erreur: Aucun document (CV/API) trouvé sur le serveur."

        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es l'assistant personnel de l'auteur de ce CV et de cette API. "
                        "Réponds UNIQUEMENT à partir du contexte ci-dessous. "
                        "Si l'information n'est pas dans le contexte, dis que tu ne sais pas.\n\n"
                        f"Contexte:\n{self.contexte}"
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        return completion.choices[0].message.content
