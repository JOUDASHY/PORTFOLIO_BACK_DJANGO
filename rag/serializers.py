from rest_framework import serializers

from .models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ["id", "role", "content", "created_at"]
        read_only_fields = ["id", "role", "created_at"]
