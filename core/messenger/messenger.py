"""
Messenger Event Handler
Processes incoming Facebook Messenger events
"""
import json
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
        logger.info("🔧 MessengerEventHandler.__init__() called")
        try:
            self.graph_api = FacebookGraphAPI()
            logger.info("✅ FacebookGraphAPI initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize FacebookGraphAPI: {e}")
            raise
        
        try:
            self.ai_service = GroqAIService()
            logger.info("✅ GroqAIService initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize GroqAIService: {e}")
            raise
    
    def handle_webhook_event(self, event_data: Dict) -> bool:
        """
        Process incoming webhook event from Facebook
        
        Args:
            event_data: Webhook event data from Facebook
            
        Returns:
            bool: True if processed successfully
        """
        logger.info("🔄 handle_webhook_event() called")
        logger.info(f"Event data: {json.dumps(event_data, indent=2)}")
        
        # Validate event structure
        object_type = event_data.get("object")
        logger.info(f"Object type: {object_type}")
        
        if object_type != "page":
            logger.warning(f"⚠️ Received non-page event: {object_type}")
            return False
        
        # Process each entry
        entries = event_data.get("entry", [])
        logger.info(f"Number of entries: {len(entries)}")
        
        for i, entry in enumerate(entries):
            logger.info(f"📋 Processing entry {i+1}/{len(entries)}")
            logger.info(f"Entry data: {json.dumps(entry, indent=2)}")
            
            messaging_events = entry.get("messaging", [])
            logger.info(f"Number of messaging events: {len(messaging_events)}")
            
            for j, messaging_event in enumerate(messaging_events):
                logger.info(f"💬 Processing messaging event {j+1}/{len(messaging_events)}")
                logger.info(f"Messaging event: {json.dumps(messaging_event, indent=2)}")
                self._process_messaging_event(messaging_event)
        
        logger.info("✅ handle_webhook_event() completed")
        return True
    
    def _process_messaging_event(self, event: Dict) -> None:
        """
        Process a single messaging event
        """
        logger.info("🔍 _process_messaging_event() called")
        
        sender_id = event.get("sender", {}).get("id")
        recipient_id = event.get("recipient", {}).get("id")  # Page ID
        
        logger.info(f"Sender ID: {sender_id}")
        logger.info(f"Recipient ID (Page ID): {recipient_id}")
        
        if not sender_id or not recipient_id:
            logger.warning("⚠️ Missing sender or recipient ID in event")
            return
        
        # Handle message event
        if "message" in event:
            logger.info("📨 Message event detected")
            self._handle_message(event["message"], sender_id, recipient_id)
        
        # Handle postback event
        elif "postback" in event:
            logger.info("🔘 Postback event detected")
            self._handle_postback(event["postback"], sender_id, recipient_id)
        
        else:
            logger.info(f"ℹ️ Unhandled event type: {list(event.keys())}")
    
    def _handle_message(self, message: Dict, sender_id: str, page_id: str) -> None:
        """
        Handle incoming message
        """
        logger.info("=" * 80)
        logger.info("📬 _handle_message() called")
        logger.info("=" * 80)
        
        message_id = message.get("mid")
        message_text = message.get("text")
        
        logger.info(f"Message ID: {message_id}")
        logger.info(f"Message text: {message_text}")
        
        if not message_text:
            logger.info("ℹ️ Ignoring message without text from {sender_id}")
            return
        
        # Check for deduplication
        if self._is_duplicate_message(message_id):
            logger.info(f"🔄 Duplicate message {message_id} ignored")
            return
        
        logger.info(f"✅ Processing NEW message from {sender_id}: {message_text[:50]}")
        
        try:
            # Mark message as seen and show typing indicator
            logger.info("👁️ Marking message as seen...")
            self.graph_api.mark_seen(sender_id)
            
            logger.info("⌨️ Showing typing indicator...")
            self.graph_api.send_typing_indicator(sender_id, typing_on=True)
            
            # Get or create conversation
            logger.info("💾 Getting/creating conversation...")
            conversation = self._get_or_create_conversation(sender_id, page_id)
            logger.info(f"Conversation ID: {conversation.id}")
            
            # Save user message
            logger.info("💾 Saving user message to database...")
            self._save_message(conversation, message_id, "user", message_text)
            
            # Get conversation history
            logger.info("📚 Retrieving conversation history...")
            history = self._get_conversation_history(conversation)
            logger.info(f"History length: {len(history)} messages")
            
            # Get AI response using RAG Service
            logger.info("🤖 Calling RAG AI Service...")
            logger.info(f"Sending to RAG: {json.dumps(history, indent=2)}")
            ai_response = self.ai_service.get_response(history, user=None)  # user=None pour Messenger (pas de User Django)
            logger.info(f"🤖 RAG response received: {ai_response[:100]}...")
            
            # Save AI response
            ai_message_id = f"ai_{message_id}"
            logger.info(f"💾 Saving AI response to database (ID: {ai_message_id})...")
            self._save_message(conversation, ai_message_id, "assistant", ai_response)
            
            # Turn off typing indicator
            logger.info("⌨️ Hiding typing indicator...")
            self.graph_api.send_typing_indicator(sender_id, typing_on=False)
            
            # Send response to user
            logger.info(f"📤 Sending response to Facebook (to user {sender_id})...")
            logger.info(f"Response to send: {ai_response[:100]}...")
            self.graph_api.send_text_message(sender_id, ai_response)
            
            logger.info(f"✅ Successfully responded to {sender_id}")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"❌ ERROR in _handle_message")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            
            # Try to send fallback message
            try:
                logger.info("🔄 Attempting to send fallback message...")
                self.graph_api.send_text_message(
                    sender_id,
                    "Désolé, une erreur s'est produite. Veuillez réessayer."
                )
                logger.info("✅ Fallback message sent")
            except Exception as e2:
                logger.error(f"❌ Failed to send fallback message: {e2}")
    
    def _handle_postback(self, postback: Dict, sender_id: str, page_id: str) -> None:
        """
        Handle postback (button clicks)
        """
        payload = postback.get("payload")
        logger.info(f"🔘 Received postback from {sender_id}: {payload}")
        
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
        
        exists = MessengerMessage.objects.filter(message_id=message_id).exists()
        logger.info(f"Duplicate check for {message_id}: {exists}")
        return exists
    
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
            logger.info(f"✅ Created new conversation for user {facebook_user_id}")
        else:
            logger.info(f"✅ Found existing conversation (ID: {conversation.id}) for user {facebook_user_id}")
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
        logger.info(f"💾 Saving message to DB: role={role}, id={message_id}, content_length={len(content)}")
        message = MessengerMessage.objects.create(
            conversation=conversation,
            message_id=message_id,
            role=role,
            content=content
        )
        logger.info(f"✅ Message saved with DB ID: {message.id}")
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
        
        logger.info(f"📚 Retrieved {len(history)} messages from conversation history")
        return history
