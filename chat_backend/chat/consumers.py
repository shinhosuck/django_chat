from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from utils.validate_user import (
    validate_community_chat_user,
    validate_private_chat_users,
    get_current_user
)
from utils.create_obj import (
    create_community_message_obj,
    create_private_message_obj
)
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.community = self.scope['url_route']['kwargs']['community']
        self.user_info = {i.split('=')[0]:i.split('=')[1] 
            for i in self.scope.get('query_string')\
            .decode()\
            .split('&')}
        self.validate = await database_sync_to_async(validate_community_chat_user)(self.user_info)

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
                'type': 'handle_event',
                'message': new_message
            }

            await self.channel_layer.group_send(
                self.community,
                event,
            )

    async def handle_event(self, event):
        await self.send(text_data=json.dumps(event['message']))

  
class ChatRoomConsumerUser(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user = await database_sync_to_async(get_current_user)(self.scope['query_string'])
        self.private_chat_room_name = ''

        self.other_user = self.scope['url_route']['kwargs']['username']

        print(self.current_user)
       
        self.validate = await database_sync_to_async(validate_private_chat_users)(
                self.current_user, 
                self.other_user
            )
        
        if 'error' in self.validate:
            await self.accept()
            await self.send(json.dumps(self.validate))
            await self.close()
        else:
            await self.accept()
            self.private_chat_room_name = self.validate['private_chat_room']

        await self.channel_layer.group_add(
            self.private_chat_room_name,
            self.channel_name
        )


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.private_chat_room_name,
            self.channel_name
        )


    async def receive(self, text_data=None, bytes_data=None):
        json_text_data = json.loads(text_data)

        new_message = await database_sync_to_async(create_private_message_obj)(
                self.current_user['user'], 
                self.other_user, 
                json_text_data['message'],
                json_text_data['respondingTo'],
            )

        event = {
            'type': 'handle_event',
            'message': new_message
        }

        await self.channel_layer.group_send(
            self.private_chat_room_name,
            event
        )

        await self.send_message_to_user(self.validate['other_user_id'],{
            'type':'handle_event', 
            'message':new_message, 
            'user':self.current_user['user']
        })


    async def handle_event(self, event):
        await self.send(text_data=json.dumps(event['message']))


    async def send_message_to_user(self, other_user_id, message_obj):
        channel_name = f'user_{other_user_id}'
        await self.channel_layer.send(channel_name, message_obj)