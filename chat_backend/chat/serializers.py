from .models import Message, ChatRoomName
from rest_framework import serializers



class ChatRoomNameSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:
        model = ChatRoomName
        fields = ['id', 'owner', 'name', 'created']

class MessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['id','chat_room', 'author', 'message', 'created']