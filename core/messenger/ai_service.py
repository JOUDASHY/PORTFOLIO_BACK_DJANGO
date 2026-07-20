"""
AI Service using RAG (Retrieval-Augmented Generation)
Uses the existing RAGService from the rag app for better responses
"""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Import the existing RAG service
_rag_service = None


def get_rag_service():
    """Get or create RAG service instance"""
    global _rag_service
    if _rag_service is None:
        from rag.services import RAGService
        logger.info("🔧 Initializing RAGService for Messenger...")
        _rag_service = RAGService()
        logger.info("✅ RAGService initialized")
    return _rag_service


class GroqAIService:
    """
    Service for interacting with AI using RAG
    Wraps the existing RAGService for Messenger compatibility
    """
    
    FALLBACK_MESSAGE = "Désolé, notre assistant est temporairement indisponible. Veuillez réessayer dans quelques instants."
    
    def __init__(self):
        logger.info("🔧 GroqAIService.__init__() called")
        # Initialize RAG service
        self.rag_service = get_rag_service()
        logger.info(f"✅ RAG service ready with {len(self.rag_service.chunks)} chunks")
    
    def get_response(self, messages: List[Dict[str, str]], user=None) -> str:
        """
        Get AI response using RAG service
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            user: Optional Django user object for personalized responses
            
        Returns:
            str: AI response text
        """
        logger.info("=" * 80)
        logger.info("🤖 GroqAIService.get_response() called")
        logger.info("=" * 80)
        
        try:
            # Get the last user message
            user_message = None
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    user_message = msg.get("content")
                    break
            
            if not user_message:
                logger.warning("⚠️ No user message found")
                return "Désolé, je n'ai pas compris votre message."
            
            logger.info(f"📤 User question: {user_message[:100]}...")
            logger.info(f"👤 User: {user if user else 'Anonymous'}")
            
            # Use RAG service to get response with full context
            logger.info("⏳ Calling RAGService.repondre()...")
            response = self.rag_service.repondre(
                question=user_message,
                user=user,
                conversation=None  # Messenger handles its own conversation history
            )
            
            logger.info(f"✅ RAG response received ({len(response)} characters)")
            logger.info(f"📥 Response preview: {response[:200]}...")
            logger.info("=" * 80)
            
            return response
            
        except Exception as e:
            logger.error("=" * 80)
            logger.error("❌ RAG SERVICE ERROR")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            logger.error("=" * 80)
            return self.FALLBACK_MESSAGE
    
    # Deprecated method - kept for backward compatibility
    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 500) -> str:
        """Legacy method - redirects to get_response()"""
        return self.get_response(messages)
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
