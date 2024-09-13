from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoomName
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import json

User = get_user_model()

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_obj = self.scope['user']
        self.chat_room_name = self.scope['url_route']['kwargs']['chat_room_name']
        user_data = self.scope.get('query_string').decode().split('&')
        self.user = {i.split('=')[0]:i.split('=')[1] for i in user_data}
        self.is_authenticated = await database_sync_to_async(self.get_user)()

        if not self.is_authenticated:
            await self.accept()
            await self.send(json.dumps(
                    {'error': 'Please login first to access websocket'}
                ))
            await self.close()
        else:
            await self.accept()

        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_room_name,
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        json_text_data = json.loads(text_data)
    
        event = {
            'type': 'handleEvent',
            'message': json_text_data['message'],
            'id': json_text_data['id']
        }

        await self.channel_layer.group_send(
            self.chat_room_name,
            event,
        )

    async def handleEvent(self, event):
        message = event.get('message')
        id = event.get('id')
        await self.send(text_data=json.dumps({'id':id, 'message':message}))

    def get_user(self):
        try:
            token_obj = Token.objects.get(key=self.user.get('token'))
        except Token.DoesNotExist:
            return False
        return token_obj.user.username == self.user.get('user')