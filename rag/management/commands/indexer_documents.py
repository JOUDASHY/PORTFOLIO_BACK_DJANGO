from django.core.management.base import BaseCommand
from rag.services import RAGService


class Command(BaseCommand):
    help = "Vérifie que le CV et la documentation API sont chargés pour l'assistant RAG"

    def handle(self, *args, **options):
        self.stdout.write("Chargement des documents RAG...")
        rag_service = RAGService()

        if not rag_service.contexte.strip():
            self.stdout.write(self.style.ERROR("Aucun document chargé (CV/API introuvables ou vides)."))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Documents chargés avec succès ({len(rag_service.contexte)} caractères)."
            )
        )
