from django.urls import path 
from .views import (
    CommunityMessagesView,
    UserMessagesView,
    ChatRoomCommunityView,
    ChatHistoryView,
    update_community_room,
    update_community_chat_session
)

app_name = 'chat'


urlpatterns = [
    path('chat/communities/', ChatRoomCommunityView.as_view(), name='chat-rooms'),
    path('community/<str:community_name>/', CommunityMessagesView.as_view(), name='community-messages'),
    path('user/<str:username>/', UserMessagesView.as_view(), name='user-messages'),
    path('chat/history/<str:username>/', ChatHistoryView.as_view(), name='chat-history'),
    path('update/community/room/', update_community_room, name='update-community-room'),
    path('update/community/chat-session/<str:username>/', update_community_chat_session, name='update-community-chat-session')
]
