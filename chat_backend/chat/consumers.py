from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from utils.validate_user import validate_user
from utils.create_obj import create_community_message_obj
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.community = self.scope['url_route']['kwargs']['community']
        self.user_info = {i.split('=')[0]:i.split('=')[1] 
            for i in self.scope.get('query_string')\
            .decode()\
            .split('&')}
        self.validate = await database_sync_to_async(validate_user)(self.user_info)

        if 'valid' in self.validate:
            await self.accept()
        else:
            await self.accept()
            await self.send(json.dumps(
                    self.validate
                ))
            await self.close()

        await self.channel_layer.group_add(
            self.community,
            self.channel_name
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.community,
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        json_text_data = json.loads(text_data)
       
        if json_text_data and json_text_data['message']:
            new_message = await database_sync_to_async(create_community_message_obj)(self.user_info, json_text_data)

            event = {
                'type': 'handleEvent',
                'message': new_message
            }

            await self.channel_layer.group_send(
                self.community,
                event,
            )

    async def handleEvent(self, event):
        await self.send(text_data=json.dumps(event['message']))

  
class ChatRoomConsumerUser(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_info = {obj.split('=')[0]:obj.split('=')[1] 
            for obj in self.scope.get('query_string')\
            .decode()\
            .split('&')}
        self.chat_recipient = self.scope['url_route']['kwargs']['user_name']
       
        self.validate = await database_sync_to_async(validate_user)(self.user_info)
        if 'valid' in self.validate:
            await self.accept()
        else:
            await self.accept()
            await self.send(json.dumps(self.validate ))
            await self.close()
