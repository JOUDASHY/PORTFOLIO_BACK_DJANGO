"""
Facebook Graph API Service
Handles communication with Facebook Messenger Platform
"""
import json
import logging
import os

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class FacebookGraphAPI:
    """
    Service for interacting with Facebook Graph API
    """
    
    GRAPH_API_VERSION = "v23.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
    
    def __init__(self):
        logger.info("🔧 FacebookGraphAPI.__init__() called")
        self.page_access_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
        if not self.page_access_token:
            logger.error("❌ FACEBOOK_PAGE_ACCESS_TOKEN environment variable is not set")
            raise ValueError("FACEBOOK_PAGE_ACCESS_TOKEN environment variable is not set")
        logger.info(f"✅ FACEBOOK_PAGE_ACCESS_TOKEN found: {self.page_access_token[:15]}...")
    
    def send_text_message(self, recipient_id: str, text: str) -> dict:
        """
        Send a text message to a Facebook Messenger user
        
        Args:
            recipient_id: Facebook PSID of the recipient
            text: Message text to send
            
        Returns:
            dict: API response
            
        Raises:
            requests.HTTPError: If the API request fails
        """
        logger.info("=" * 80)
        logger.info("📤 send_text_message() called")
        logger.info("=" * 80)
        logger.info(f"Recipient ID: {recipient_id}")
        logger.info(f"Message text: {text[:100]}...")
        
        url = f"{self.BASE_URL}/me/messages"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text},
        }
        
        logger.info(f"API URL: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            logger.info("⏳ Sending POST request to Facebook Graph API...")
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            response_data = response.json()
            logger.info(f"✅ Message sent successfully to {recipient_id}")
            logger.info(f"Response data: {json.dumps(response_data, indent=2)}")
            logger.info("=" * 80)
            return response_data
            
        except requests.HTTPError as e:
            logger.error("=" * 80)
            logger.error("❌ FACEBOOK API HTTP ERROR")
            logger.error("=" * 80)
            logger.error(f"Status code: {e.response.status_code}")
            logger.error(f"Response text: {e.response.text}")
            logger.error(f"Response headers: {dict(e.response.headers)}")
            logger.error("=" * 80)
            raise
        except Exception as e:
            logger.error("=" * 80)
            logger.error("❌ UNEXPECTED ERROR sending message")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            logger.error("=" * 80)
            raise
    
    def send_typing_indicator(self, recipient_id: str, typing_on: bool = True) -> dict:
        """
        Send typing indicator (for better UX)
        
        Args:
            recipient_id: Facebook PSID
            typing_on: True to show typing, False to hide
        """
        logger.info(f"⌨️ send_typing_indicator({recipient_id}, typing_on={typing_on})")
        
        url = f"{self.BASE_URL}/me/messages"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "recipient": {"id": recipient_id},
            "sender_action": "typing_on" if typing_on else "typing_off",
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"✅ Typing indicator {'shown' if typing_on else 'hidden'}")
            return response.json()
        except Exception as e:
            logger.warning(f"⚠️ Failed to send typing indicator: {str(e)}")
            return {}
    
    def mark_seen(self, recipient_id: str) -> dict:
        """
        Mark message as seen
        """
        logger.info(f"👁️ mark_seen({recipient_id})")
        
        url = f"{self.BASE_URL}/me/messages"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "recipient": {"id": recipient_id},
            "sender_action": "mark_seen",
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info("✅ Message marked as seen")
            return response.json()
        except Exception as e:
            logger.warning(f"⚠️ Failed to mark as seen: {str(e)}")
            return {}
