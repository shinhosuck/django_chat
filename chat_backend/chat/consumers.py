from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.user_obj = self.scope['user']
        self.chat_room_name = self.scope['url_route']['kwargs']['chat_room_name']
        
        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_room_name,
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        json_text_data = json.loads(text_data)['message']
    
        event = {
            'type': 'handleEvent',
            'message': json_text_data
        }

        await self.channel_layer.group_send(
            self.chat_room_name,
            event,
        )

    async def handleEvent(self, event):
        message = event.get('message')
        await self.send(text_data=json.dumps({'message':message}))