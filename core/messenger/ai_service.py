"""
AI Service using Groq
Handles conversation with the AI model
"""
import logging
import os
from typing import List, Dict

from groq import Groq

logger = logging.getLogger(__name__)


class GroqAIService:
    """
    Service for interacting with Groq AI API
    """
    
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    FALLBACK_MESSAGE = "Désolé, notre assistant est temporairement indisponible. Veuillez réessayer dans quelques instants."
    
    def __init__(self):
        logger.info("🔧 GroqAIService.__init__() called")
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("❌ GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        logger.info(f"✅ GROQ_API_KEY found: {api_key[:10]}...")
        self.client = Groq(api_key=api_key)
        self.model = os.environ.get("GROQ_MODEL", self.DEFAULT_MODEL)
        logger.info(f"✅ Using Groq model: {self.model}")
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI assistant
        Can be customized based on your needs
        """
        return """Tu es un assistant virtuel intelligent et serviable qui représente le portfolio de Nilsen Un-it.
        
INFORMATIONS IMPORTANTES:
- Nilsen Un-it est un développeur Full Stack
- Portfolio: https://portfolio.unityfianar.site
- Compétences: Django, React, Python, JavaScript, MySQL, PostgreSQL, Docker, Git
- Expérience en développement web backend et frontend

Tu es là pour:
- Répondre aux questions sur les compétences et l'expérience de Nilsen
- Aider les visiteurs à naviguer dans le portfolio
- Fournir des informations PRÉCISES sur les projets réalisés
- Être professionnel, courtois et utile

IMPORTANT: Si on te demande les projets, réponds que tu peux consulter le portfolio sur https://portfolio.unityfianar.site 
ou demande à l'utilisateur de préciser quel type de projet l'intéresse.

Réponds de manière concise et claire. Si tu ne sais pas quelque chose, dis-le honnêtement."""
    
    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 500) -> str:
        """
        Send a chat request to Groq API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens in response
            
        Returns:
            str: AI response text
        """
        logger.info("=" * 80)
        logger.info("🤖 GroqAIService.chat() called")
        logger.info("=" * 80)
        
        try:
            # Add system prompt if not already present
            if not messages or messages[0].get("role") != "system":
                system_prompt = self.get_system_prompt()
                messages.insert(0, {
                    "role": "system",
                    "content": system_prompt
                })
                logger.info(f"✅ System prompt added (length: {len(system_prompt)})")
            
            logger.info(f"📤 Calling Groq API with {len(messages)} messages")
            logger.info(f"Model: {self.model}")
            logger.info(f"Max tokens: {max_tokens}")
            
            # Call Groq API
            logger.info("⏳ Sending request to Groq...")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )
            logger.info("✅ Response received from Groq")
            
            response_text = completion.choices[0].message.content
            logger.info(f"📥 Groq response length: {len(response_text)} characters")
            logger.info(f"📥 Groq response preview: {response_text[:200]}...")
            logger.info("=" * 80)
            
            return response_text
            
        except Exception as e:
            logger.error("=" * 80)
            logger.error("❌ GROQ API ERROR")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            logger.info(f"🔄 Returning fallback message")
            logger.error("=" * 80)
            return self.FALLBACK_MESSAGE
    
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Simple wrapper around chat() for consistency
        """
        return self.chat(messages)
    
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
