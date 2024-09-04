from django.contrib import admin
from .models import ChatRoomName, Message 


@admin.register(ChatRoomName)
class ChatRoomNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'chat_room', 'created']