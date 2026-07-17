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
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        self.client = Groq(api_key=api_key)
        self.model = os.environ.get("GROQ_MODEL", self.DEFAULT_MODEL)
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI assistant
        Can be customized based on your needs
        """
        return """Tu es un assistant virtuel intelligent et serviable qui représente le portfolio de Nilsen.
        
Tu es là pour:
- Répondre aux questions sur les compétences et l'expérience de Nilsen
- Aider les visiteurs à naviguer dans le portfolio
- Fournir des informations sur les projets réalisés
- Être professionnel, courtois et utile

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
        try:
            # Add system prompt if not already present
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {
                    "role": "system",
                    "content": self.get_system_prompt()
                })
            
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )
            
            response_text = completion.choices[0].message.content
            logger.info(f"Groq API response generated successfully")
            return response_text
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
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
