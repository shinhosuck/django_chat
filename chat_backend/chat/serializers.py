from .models import (
    CommunityMessage, 
    ChatRoomCommunity,
    UserMessage,
    ChatHistory
)
from rest_framework import serializers
from django.contrib.auth import get_user_model 

User = get_user_model()

class ChatRoomCommunitySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    messages = serializers.SerializerMethodField(read_only=True, method_name='get_messages')
    class Meta:
        model = ChatRoomCommunity
        fields = ['id', 'owner', 'name', 'created', 'messages']

    def get_messages(self, obj):
        serializer =CommunityMessageSerializer(obj.messages.all(), many=True)
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


class ChatHistorySerializer(serializers.ModelSerializer):
    communities = serializers.SerializerMethodField(method_name='get_communities', read_only=True)
    users = serializers.SerializerMethodField(method_name='get_users', read_only=True)
    last_chat_date_community = serializers.SerializerMethodField(
            method_name='get_last_chat_date_community', 
            read_only=True
        )
    last_chat_date_user = serializers.SerializerMethodField(
            method_name='get_last_chat_users',
            read_only=True
        )
    class Meta:
        model = ChatHistory
        fields = [
            'user', 
            'communities', 
            'last_chat_date_community', 
            'users', 
            'last_chat_date_user'
        ]

    def get_communities(self, obj):
        communities = list(obj.communities.all().values_list('name', flat=True))
        return communities
    
    def get_last_chat_date_community(self, obj):
        user = self.context.get('request').user
        communities = self.get_communities(obj)
        last_chat_dates = {}

        for community in communities:
            created = CommunityMessage.objects.filter(author=user, community__name=community)\
                .order_by('-created').first().created
            last_chat_dates[community] = str(created)
        return last_chat_dates

    def get_users(self, obj):
        users = list(obj.users.all().values_list('username', flat=True))
        return users

    def get_last_chat_users(self, obj):
        user = self.context.get('request').user
        users = self.get_users(obj)
       
        last_chat_dates = {}

        for username in users:
            user_obj = User.objects.get(username=username)
            created = UserMessage.objects.filter(user=user, recipient=user_obj)\
                .order_by('-created').first().created
            last_chat_dates[username] = str(created)
        return last_chat_dates
            