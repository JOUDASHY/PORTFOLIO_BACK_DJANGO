"""
Facebook Messenger Webhook Views
Handles GET (verification) and POST (events) requests from Facebook
"""
import json
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
        logger.info("=" * 80)
        logger.info("🔍 WEBHOOK GET REQUEST - VERIFICATION")
        logger.info("=" * 80)
        logger.info(f"Query params: {dict(request.GET)}")
        
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        verify_token = os.environ.get("FACEBOOK_VERIFY_TOKEN")
        
        logger.info(f"Mode: {mode}")
        logger.info(f"Challenge: {challenge}")
        logger.info(f"Token received: {token[:10] if token else 'None'}...")
        logger.info(f"Token expected: {verify_token[:10] if verify_token else 'None'}...")
        
        if not verify_token:
            logger.error("❌ FACEBOOK_VERIFY_TOKEN environment variable not set")
            return HttpResponse("Error: verify token not configured", status=500)
        
        # Verify the token matches
        if mode == "subscribe" and token == verify_token:
            logger.info("✅ Webhook verified successfully - Returning challenge")
            return HttpResponse(challenge, status=200)
        else:
            logger.warning(f"❌ Webhook verification failed. Mode: {mode}, Token match: {token == verify_token}")
            return HttpResponse("Verification failed", status=403)
    
    def post(self, request):
        """
        Receive and process Messenger events
        """
        logger.info("=" * 80)
        logger.info("📨 WEBHOOK POST REQUEST - EVENT RECEIVED")
        logger.info("=" * 80)
        
        try:
            # Log request details
            logger.info(f"Method: {request.method}")
            logger.info(f"Path: {request.path}")
            logger.info(f"Content-Type: {request.content_type}")
            
            # Log headers (sans tokens sensibles)
            headers = dict(request.headers)
            sensitive_headers = ['Authorization', 'X-Hub-Signature', 'X-Hub-Signature-256']
            safe_headers = {k: ('***' if k in sensitive_headers else v) for k, v in headers.items()}
            logger.info(f"Headers: {json.dumps(safe_headers, indent=2)}")
            
            # Log raw body
            try:
                raw_body = request.body.decode('utf-8')
                logger.info(f"Raw body length: {len(raw_body)} bytes")
                logger.info(f"Raw body: {raw_body[:500]}...")  # Premier 500 caractères
            except Exception as e:
                logger.warning(f"Could not decode raw body: {e}")
            
            # Log parsed data
            data = request.data
            logger.info(f"Parsed data: {json.dumps(data, indent=2)}")
            
            # Initialize event handler
            logger.info("🔧 Initializing MessengerEventHandler...")
            handler = MessengerEventHandler()
            
            # Process the event
            logger.info("⚙️ Processing webhook event...")
            success = handler.handle_webhook_event(data)
            
            if success:
                logger.info("✅ Event processed successfully")
                # Always return 200 to Facebook to acknowledge receipt
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
            else:
                logger.warning("⚠️ Event processing returned False")
                return Response({"status": "ok"}, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"❌ CRITICAL ERROR in webhook POST")
            logger.error("=" * 80)
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error message: {str(e)}", exc_info=True)
            # Still return 200 to prevent Facebook from retrying
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_200_OK)
