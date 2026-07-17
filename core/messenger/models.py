"""
Models for Facebook Messenger Integration
Stores conversation history between users and the AI bot
"""
from django.db import models


class MessengerConversation(models.Model):
    """
    Conversation thread with a Facebook Messenger user
    """
    facebook_user_id = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Facebook PSID (Page-Scoped ID) of the user"
    )
    page_id = models.CharField(
        max_length=255,
        help_text="Facebook Page ID"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Messenger Conversation"
        verbose_name_plural = "Messenger Conversations"
        unique_together = ["facebook_user_id", "page_id"]
        ordering = ["-updated_at"]
    
    def __str__(self):
        return f"Conversation {self.facebook_user_id[:10]}... on Page {self.page_id}"


class MessengerMessage(models.Model):
    """
    Individual message in a conversation
    """
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]
    
    conversation = models.ForeignKey(
        MessengerConversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    message_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Facebook message ID (mid) for deduplication"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Messenger Message"
        verbose_name_plural = "Messenger Messages"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["message_id"]),
            models.Index(fields=["conversation", "created_at"]),
        ]
    
    def __str__(self):
        return f"[{self.role}] {self.content[:50]}..."
