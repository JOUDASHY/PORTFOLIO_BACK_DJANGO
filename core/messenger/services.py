"""
Facebook Graph API Service
Handles communication with Facebook Messenger Platform
"""
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
        self.page_access_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
        if not self.page_access_token:
            raise ValueError("FACEBOOK_PAGE_ACCESS_TOKEN environment variable is not set")
    
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
        url = f"{self.BASE_URL}/me/messages"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text},
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Message sent to {recipient_id}")
            return response.json()
        except requests.HTTPError as e:
            logger.error(f"Failed to send message: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending message: {str(e)}")
            raise
    
    def send_typing_indicator(self, recipient_id: str, typing_on: bool = True) -> dict:
        """
        Send typing indicator (for better UX)
        
        Args:
            recipient_id: Facebook PSID
            typing_on: True to show typing, False to hide
        """
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
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to send typing indicator: {str(e)}")
            return {}
    
    def mark_seen(self, recipient_id: str) -> dict:
        """
        Mark message as seen
        """
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
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to mark as seen: {str(e)}")
            return {}
