from django.conf import settings
from django.db import models


class ChatHistory(models.Model):
    ROLE_CHOICES = [
        ("user", "Utilisateur"),
        ("assistant", "Assistant"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message de chat"
        verbose_name_plural = "Messages de chat"

    def __str__(self):
        return f"[{self.role}] {self.user.username} - {self.content[:50]}"
