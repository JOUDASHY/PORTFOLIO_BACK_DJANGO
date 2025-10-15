from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from core.models import Notification, Visit
from core.serializers import NotificationSerializer


@api_view(["DELETE"])
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return Response({"status": "success", "message": "All notifications cleared."})


@api_view(["POST"])
def mark_all_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return Response({"status": "success", "message": "All notifications marked as read."})


class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        notifications_data = [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at,
            }
            for n in notifications
        ]
        return Response(notifications_data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        title = request.data.get('title')
        message = request.data.get('message')
        if not title or not message:
            return Response({"error": "Le titre et le message sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)
        Notification.objects.create(user=user, title=title, message=message)
        return Response({"message": "Notification créée avec succès."}, status=status.HTTP_201_CREATED)

    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marquée comme lue."}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)


class NotificationTriggerView(APIView):
    def post(self, request):
        user = request.user
        event_type = request.data.get('event_type')
        project_id = request.data.get('project_id')

        if event_type == 'rating':
            Notification.objects.create(
                user=user,
                title="Nouveau vote reçu",
                message=f"Un internaute a noté votre projet ID {project_id}."
            )
            return Response({"message": "Notification créée pour une nouvelle note."}, status=status.HTTP_201_CREATED)

        elif event_type == 'view':
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            visits_count = Visit.objects.filter(timestamp__range=(yesterday, today)).count()
            if visits_count >= 5:
                Notification.objects.create(
                    user=user,
                    title="Vues atteintes",
                    message=f"Votre projet a reçu {visits_count} vues en une journée."
                )
                return Response({"message": "Notification créée pour les vues."}, status=status.HTTP_201_CREATED)

        return Response({"error": "Type d'événement non valide."}, status=status.HTTP_400_BAD_REQUEST)


class NotificationCreateBroadcastView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save(user=request.user)
        channel_layer = get_channel_layer()
        group_name = f"notifications_{request.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": {
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": str(notification.created_at),
                },
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


