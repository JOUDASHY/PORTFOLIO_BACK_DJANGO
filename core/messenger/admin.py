"""
Django Admin configuration for Messenger models
"""
from django.contrib import admin

from .models import MessengerConversation, MessengerMessage


@admin.register(MessengerConversation)
class MessengerConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "facebook_user_id", "page_id", "created_at", "updated_at"]
    list_filter = ["page_id", "created_at"]
    search_fields = ["facebook_user_id", "page_id"]
    readonly_fields = ["created_at", "updated_at"]
    
    def has_add_permission(self, request):
        return False  # Don't allow manual creation


@admin.register(MessengerMessage)
class MessengerMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "conversation", "role", "content_preview", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["content", "message_id", "conversation__facebook_user_id"]
    readonly_fields = ["message_id", "conversation", "role", "content", "created_at"]
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Content"
    
    def has_add_permission(self, request):
        return False  # Don't allow manual creation
    
    def has_change_permission(self, request, obj=None):
        return False  # Read-only
