"""
AI Service using RAG (Retrieval-Augmented Generation)
Utilise le service RAG existant pour des réponses intelligentes
"""
import logging
from typing import List, Dict

# Importer le RAG Service existant
from rag.services import RAGService

logger = logging.getLogger(__name__)


class GroqAIService:
    """
    Service for interacting with Groq AI API via RAG
    Utilise votre CV, API doc, et toutes vos données BDD
    """
    
    def __init__(self):
        logger.info("🔧 GroqAIService.__init__() called")
        # Utiliser le RAG Service existant
        self.rag_service = RAGService()
        logger.info("✅ RAG Service initialized with CV, API docs, and database access")
    
    def get_response(self, messages: List[Dict[str, str]], user=None) -> str:
        """
        Get response using RAG Service
        
        Args:
            messages: List of message dictionaries
            user: Django User object (pour accès BDD)
            
        Returns:
            str: AI response with full context
        """
        logger.info("=" * 80)
        logger.info("🤖 get_response() called - Using RAG Service")
        logger.info("=" * 80)
        
        try:
            # Extraire le dernier message utilisateur
            user_message = ""
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    user_message = msg.get("content", "")
                    break
            
            if not user_message:
                logger.warning("⚠️ No user message found")
                return "Désolé, je n'ai pas compris votre message."
            
            logger.info(f"📤 User question: {user_message[:100]}...")
            logger.info("⏳ Calling RAG Service with CV, API docs, and DB access...")
            
            # Appeler le RAG Service
            response = self.rag_service.repondre(
                question=user_message,
                user=user,
                conversation=None  # Messenger gère son propre historique
            )
            
            logger.info(f"📥 RAG response length: {len(response)} characters")
            logger.info(f"� RAG response preview: {response[:200]}...")
            logger.info("=" * 80)
            
            return response
            
        except Exception as e:
            logger.error("=" * 80)
            logger.error("❌ RAG SERVICE ERROR")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            logger.error("=" * 80)
            return "Désolé, une erreur s'est produite. Veuillez réessayer."
            logger.info(f"🔄 Returning fallback message")
            logger.error("=" * 80)
            return self.FALLBACK_MESSAGE
    
    def prepare_conversation_history(
        self, 
        conversation_messages: List[tuple], 
        max_history: int = 10
    ) -> List[Dict[str, str]]:
        """
        Prepare conversation history for Groq API
        
        Args:
            conversation_messages: List of (role, content) tuples from database
            max_history: Maximum number of messages to include
            
        Returns:
            List of message dictionaries
        """
        # Keep only the last N messages for context
        recent_messages = conversation_messages[-max_history:]
        
        return [
            {"role": role, "content": content}
            for role, content in recent_messages
        ]
