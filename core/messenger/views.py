"""
Facebook Messenger Webhook Views
Handles GET (verification) and POST (events) requests from Facebook
"""
import logging
import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .messenger import MessengerEventHandler

logger = logging.getLogger(__name__)


class FacebookWebhookView(APIView):
    """
    Webhook endpoint for Facebook Messenger
    
    GET: Webhook verification by Facebook
    POST: Receive messaging events
    """
    
    # Allow POST without CSRF token (Facebook doesn't have it)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        """
        Webhook verification by Facebook
        
        Facebook sends:
        - hub.mode=subscribe
        - hub.verify_token=YOUR_VERIFY_TOKEN
        - hub.challenge=RANDOM_STRING
        
        We must return hub.challenge if verify_token matches
        """
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        verify_token = os.environ.get("FACEBOOK_VERIFY_TOKEN")
        
        if not verify_token:
            logger.error("FACEBOOK_VERIFY_TOKEN environment variable not set")
            return HttpResponse("Error: verify token not configured", status=500)
        
        # Verify the token matches
        if mode == "subscribe" and token == verify_token:
            logger.info("Webhook verified successfully")
            return HttpResponse(challenge, status=200)
        else:
            logger.warning(f"Webhook verification failed. Mode: {mode}, Token match: {token == verify_token}")
            return HttpResponse("Verification failed", status=403)
    
    def post(self, request):
        """
        Receive and process Messenger events
        """
        try:
            data = request.data
            logger.info(f"Received webhook event: {data}")
            
            # Initialize event handler
            handler = MessengerEventHandler()
            
            # Process the event
            success = handler.handle_webhook_event(data)
            
            if success:
                # Always return 200 to Facebook to acknowledge receipt
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
            else:
                logger.warning("Event processing returned False")
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Error processing webhook event: {str(e)}", exc_info=True)
            # Still return 200 to prevent Facebook from retrying
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_200_OK)
