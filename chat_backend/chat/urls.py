from django.urls import path 
from .views import (
    CommunityMessagesView,
    UserMessagesView,
    ChatRoomCommunityView,
    ChatHistoryView
)

app_name = 'chat'


urlpatterns = [
    path('chat/communities/', ChatRoomCommunityView.as_view(), name='chat-rooms'),
    path('community/<str:community_name>/', CommunityMessagesView.as_view(), name='community-messages'),
    path('user/<str:username>/', UserMessagesView.as_view(), name='user-messages'),
    path('chat/history/<str:username>/', ChatHistoryView.as_view(), name='chat-history')
]
