# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Cette méthode est appelée lorsque la connexion WebSocket est établie
        self.user = self.scope['user']
        self.group_name = f'notifications_{self.user.id}'

        # Joindre un groupe spécifique à l'utilisateur
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Cette méthode est appelée lorsque la connexion WebSocket est fermée
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Cette méthode est appelée lorsqu'un message est reçu du client
        data = json.loads(text_data)
        message = data['message']

        # Envoyer un message au groupe
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'notification_message',
                'message': message
            }
        )

    async def notification_message(self, event):
        # Cette méthode est appelée pour envoyer un message à WebSocket
        message = event['message']

        # Envoyer le message au client WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
