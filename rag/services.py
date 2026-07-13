import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from django.conf import settings
import pdfplumber
import json
import os

class RAGService:
    def __init__(self):
        # We ensure the persistence directory exists
        if not os.path.exists(settings.CHROMA_PERSIST_DIR):
            os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
            
        self.client_chroma = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client_chroma.get_or_create_collection(
            name="mon_profil",
            embedding_function=self.embedding_fn
        )
        
        # Groq client will fail if GROQ_API_KEY is not set, so we can initialize it here
        # But for robustness, we check it before calling.
        api_key = getattr(settings, 'GROQ_API_KEY', None)
        if api_key:
            self.groq_client = Groq(api_key=api_key)
        else:
            self.groq_client = None

    # --- Extraction ---

    def extraire_cv(self, chemin_pdf):
        texte = ""
        try:
            with pdfplumber.open(chemin_pdf) as pdf:
                for page in pdf.pages:
                    texte += page.extract_text() + "\n"
        except Exception as e:
            print(f"Erreur extraction CV: {e}")
        return texte

    def extraire_doc_api(self, chemin_json_ou_md):
        texte = ""
        try:
            # Simple handle for markdown if json is not provided
            if chemin_json_ou_md.endswith('.md'):
                with open(chemin_json_ou_md, 'r', encoding='utf-8') as f:
                    texte = f.read()
            else:
                with open(chemin_json_ou_md, 'r', encoding='utf-8') as f:
                    spec = json.load(f)
                for route, methodes in spec.get('paths', {}).items():
                    for methode, details in methodes.items():
                        texte += f"Route: {methode.upper()} {route}\n"
                        texte += f"Description: {details.get('summary', details.get('description', ''))}\n\n"
        except Exception as e:
            print(f"Erreur extraction API: {e}")
        return texte

    # --- Découpage en chunks ---

    def decouper_en_chunks(self, texte, taille=500, overlap=50):
        chunks = []
        i = 0
        while i < len(texte):
            chunks.append(texte[i:i + taille])
            i += taille - overlap
        return chunks

    # --- Indexation ---

    def indexer_documents(self, chemin_cv, chemin_api):
        cv_texte = self.extraire_cv(chemin_cv)
        api_texte = self.extraire_doc_api(chemin_api)

        chunks_cv = [(c, "CV") for c in self.decouper_en_chunks(cv_texte)] if cv_texte else []
        chunks_api = [(c, "API") for c in self.decouper_en_chunks(api_texte)] if api_texte else []
        tous_chunks = chunks_cv + chunks_api
        
        if not tous_chunks:
            return 0

        ids = [f"chunk_{i}" for i in range(len(tous_chunks))]
        documents = [c[0] for c in tous_chunks]
        metadatas = [{"source": c[1]} for c in tous_chunks]

        # Reset la collection avant réindexation
        try:
            self.client_chroma.delete_collection("mon_profil")
        except:
            pass
            
        self.collection = self.client_chroma.get_or_create_collection(
            name="mon_profil",
            embedding_function=self.embedding_fn
        )

        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
        return len(tous_chunks)

    # --- Recherche + génération ---

    def rechercher_contexte(self, question, k=4):
        resultats = self.collection.query(query_texts=[question], n_results=k)
        if not resultats['documents'] or not resultats['documents'][0]:
            return ""
        return "\n\n".join(resultats['documents'][0])

    def repondre(self, question):
        if not self.groq_client:
            return "Erreur: Clé API Groq non configurée sur le serveur."
            
        contexte = self.rechercher_contexte(question)

        completion = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""Tu es l'assistant personnel de l'auteur de ce CV et de cette API. Tu réponds aux questions sur le profil et l'API en te basant UNIQUEMENT sur le contexte fourni.
Si l'information n'est pas dans le contexte, dis que tu ne sais pas.

Contexte:
{contexte}"""
                },
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message.content
