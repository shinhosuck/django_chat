from .models import Message, ChatRoomName
from rest_framework import serializers



class ChatRoomNameSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    messages = serializers.SerializerMethodField(read_only=True, method_name='get_messages')
    class Meta:
        model = ChatRoomName
        fields = ['id', 'owner', 'name', 'created', 'messages']

    def get_messages(self, obj):
        serializer = MessageSerializer(obj.messages.all(),many=True)
        return serializer.data
    

class MessageSerializer(serializers.ModelSerializer):
    chat_room = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['id','chat_room', 'author', 'message', 'created']