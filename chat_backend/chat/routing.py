from .consumers import ChatRoomConsumer
from django.urls import path 


websocket_urlpatterns = [
    path('ws/chat/room/<chat_room_name>/', ChatRoomConsumer.as_asgi())
]