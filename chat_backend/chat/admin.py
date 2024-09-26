from django.contrib import admin
from .models import (
    ChatRoomCommunity, 
    CommunityMessage, 
    UserMessage,
    ChatHistory
)


@admin.register(ChatRoomCommunity)
class ChatRoomCommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created']

@admin.register(CommunityMessage)
class CommunityMessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'community', 'created']

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'other_user', 'created']

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user']