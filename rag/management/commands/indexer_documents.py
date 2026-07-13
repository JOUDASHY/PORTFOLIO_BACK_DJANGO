from django.core.management.base import BaseCommand
from rag.services import RAGService
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Indexe le CV et la documentation API dans ChromaDB"

    def handle(self, *args, **options):
        self.stdout.write("Initialisation du service RAG...")
        rag_service = RAGService()
        
        # Racine du projet Django
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        
        chemin_cv = os.path.join(base_dir, 'CV_Eddy_Nilsen.pdf')
        chemin_api = os.path.join(base_dir, 'API_DOCUMENTATION.md')
        
        # Verify files exist
        if not os.path.exists(chemin_cv):
            self.stdout.write(self.style.WARNING(f"Fichier introuvable: {chemin_cv}"))
            chemin_cv = ""
            
        if not os.path.exists(chemin_api):
            self.stdout.write(self.style.WARNING(f"Fichier introuvable: {chemin_api}"))
            chemin_api = ""

        if not chemin_cv and not chemin_api:
            self.stdout.write(self.style.ERROR("Aucun document trouvé pour l'indexation."))
            return

        self.stdout.write("Indexation en cours...")
        nb_chunks = rag_service.indexer_documents(
            chemin_cv=chemin_cv,
            chemin_api=chemin_api
        )
        self.stdout.write(self.style.SUCCESS(f"{nb_chunks} chunks indexés avec succès."))
