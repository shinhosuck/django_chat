from .consumers import (
     ChatRoomConsumer, 
     ChatRoomConsumerUser
)
from django.urls import path 


websocket_urlpatterns = [
    path('ws/chat/room/<community>/', ChatRoomConsumer.as_asgi()),
    path('ws/chat/user/<username>/', ChatRoomConsumerUser.as_asgi())
]