from .models import (
    CommunityMessage, 
    ChatRoomCommunity,
    UserMessage,
    ChatHistory
)
from rest_framework import serializers



class ChatRoomCommunitySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    messages = serializers.SerializerMethodField(read_only=True, method_name='get_messages')
    class Meta:
        model = ChatRoomCommunity
        fields = ['id', 'owner', 'name', 'created', 'messages']

    def get_messages(self, obj):
        serializer =CommunityMessageSerializer(obj.messages.all(),many=True)
        return serializer.data
    

class CommunityMessageSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        model = CommunityMessage
        fields = ['id', 'community', 'author', 'message', 'created']


class UserMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    class Meta:
        model = UserMessage 
        fields = ['id', 'user', 'recipient', 'message', 'created']


class ChatHitorySerializer(serializers.ModelSerializer):
    communities = serializers.SerializerMethodField(method_name='get__community', read_only=True)
    last_chat_date_community = serializers.SerializerMethodField(
            method_name='get_last_chat_date_community', 
            read_only=True
        )
    class Meta:
        model = ChatHistory
        fields = ['user', 'communities', 'users', 'last_chat_date_community']

    def get__community(self, obj):
        communities = list(obj.communities.all().values_list('name', flat=True))
        return communities
    
    def get_last_chat_date_community(self, obj):
        communities = list(obj.communities.all().values_list('name', flat=True))
        get_last_chat_date_community = [str(CommunityMessage.objects.filter(community__name=community)\
        .order_by('-created').values_list('created', flat=True).first()) for community in communities]
        return dict(zip(communities, get_last_chat_date_community))