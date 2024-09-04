from django.urls import path 
from .views import (
    messages_view,
    chat_room_names_view
)

app_name = 'chat'


urlpatterns = [
    path('chat/rooms/', chat_room_names_view, name='chat-rooms'),
    path('messages/', messages_view, name='all-messages'),
]
