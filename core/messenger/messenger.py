"""
Messenger Event Handler
Processes incoming Facebook Messenger events
"""
import logging
from typing import Dict, Optional

from .ai_service import GroqAIService
from .models import MessengerConversation, MessengerMessage
from .services import FacebookGraphAPI

logger = logging.getLogger(__name__)


class MessengerEventHandler:
    """
    Handles incoming Messenger events and coordinates the response pipeline
    """
    
    def __init__(self):
        self.graph_api = FacebookGraphAPI()
        self.ai_service = GroqAIService()
    
    def handle_webhook_event(self, event_data: Dict) -> bool:
        """
        Process incoming webhook event from Facebook
        
        Args:
            event_data: Webhook event data from Facebook
            
        Returns:
            bool: True if processed successfully
        """
        # Validate event structure
        if event_data.get("object") != "page":
            logger.warning(f"Received non-page event: {event_data.get('object')}")
            return False
        
        # Process each entry
        entries = event_data.get("entry", [])
        for entry in entries:
            messaging_events = entry.get("messaging", [])
            for messaging_event in messaging_events:
                self._process_messaging_event(messaging_event)
        
        return True
    
    def _process_messaging_event(self, event: Dict) -> None:
        """
        Process a single messaging event
        """
        sender_id = event.get("sender", {}).get("id")
        recipient_id = event.get("recipient", {}).get("id")  # Page ID
        
        if not sender_id or not recipient_id:
            logger.warning("Missing sender or recipient ID in event")
            return
        
        # Handle message event
        if "message" in event:
            self._handle_message(event["message"], sender_id, recipient_id)
        
        # Handle postback event
        elif "postback" in event:
            self._handle_postback(event["postback"], sender_id, recipient_id)
    
    def _handle_message(self, message: Dict, sender_id: str, page_id: str) -> None:
        """
        Handle incoming message
        """
        message_id = message.get("mid")
        message_text = message.get("text")
        
        if not message_text:
            logger.info(f"Ignoring message without text from {sender_id}")
            return
        
        # Check for deduplication
        if self._is_duplicate_message(message_id):
            logger.info(f"Duplicate message {message_id} ignored")
            return
        
        logger.info(f"Processing message from {sender_id}: {message_text[:50]}")
        
        try:
            # Mark message as seen and show typing indicator
            self.graph_api.mark_seen(sender_id)
            self.graph_api.send_typing_indicator(sender_id, typing_on=True)
            
            # Get or create conversation
            conversation = self._get_or_create_conversation(sender_id, page_id)
            
            # Save user message
            self._save_message(conversation, message_id, "user", message_text)
            
            # Get conversation history
            history = self._get_conversation_history(conversation)
            
            # Get AI response
            ai_response = self.ai_service.chat(history)
            
            # Save AI response
            ai_message_id = f"ai_{message_id}"
            self._save_message(conversation, ai_message_id, "assistant", ai_response)
            
            # Turn off typing indicator
            self.graph_api.send_typing_indicator(sender_id, typing_on=False)
            
            # Send response to user
            self.graph_api.send_text_message(sender_id, ai_response)
            
            logger.info(f"Successfully responded to {sender_id}")
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Try to send fallback message
            try:
                self.graph_api.send_text_message(
                    sender_id,
                    "Désolé, une erreur s'est produite. Veuillez réessayer."
                )
            except:
                pass
    
    def _handle_postback(self, postback: Dict, sender_id: str, page_id: str) -> None:
        """
        Handle postback (button clicks)
        """
        payload = postback.get("payload")
        logger.info(f"Received postback from {sender_id}: {payload}")
        
        # You can handle specific postback payloads here
        # For now, treat it as a regular message
        if payload:
            self._handle_message(
                {"mid": f"postback_{payload}", "text": payload},
                sender_id,
                page_id
            )
    
    def _is_duplicate_message(self, message_id: str) -> bool:
        """
        Check if message already exists (deduplication)
        """
        if not message_id:
            return False
        return MessengerMessage.objects.filter(message_id=message_id).exists()
    
    def _get_or_create_conversation(
        self, 
        facebook_user_id: str, 
        page_id: str
    ) -> MessengerConversation:
        """
        Get existing conversation or create a new one
        """
        conversation, created = MessengerConversation.objects.get_or_create(
            facebook_user_id=facebook_user_id,
            page_id=page_id
        )
        if created:
            logger.info(f"Created new conversation for user {facebook_user_id}")
        return conversation
    
    def _save_message(
        self,
        conversation: MessengerConversation,
        message_id: str,
        role: str,
        content: str
    ) -> MessengerMessage:
        """
        Save message to database
        """
        message = MessengerMessage.objects.create(
            conversation=conversation,
            message_id=message_id,
            role=role,
            content=content
        )
        return message
    
    def _get_conversation_history(
        self,
        conversation: MessengerConversation,
        max_messages: int = 10
    ) -> list:
        """
        Get recent conversation history for AI context
        """
        messages = conversation.messages.order_by("-created_at")[:max_messages]
        messages = list(reversed(messages))  # Oldest first
        
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        return history
