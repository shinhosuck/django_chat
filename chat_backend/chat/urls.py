from django.urls import path 
from .views import (
    messages_view,
    ChatRoomNamesView
)

app_name = 'chat'


urlpatterns = [
    path('chat/rooms/', ChatRoomNamesView.as_view(), name='chat-rooms'),
    path('messages/', messages_view, name='all-messages'),
]
