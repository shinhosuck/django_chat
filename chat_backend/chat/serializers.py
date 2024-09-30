from .models import (
    CommunityMessage, 
    ChatRoomCommunity,
    UserMessage,
    ChatHistory
)
from accounts.serializers import ProfileSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model 

User = get_user_model()

class ChatRoomCommunitySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    users_in_the_room = serializers.SerializerMethodField(read_only=True, method_name='get_users_inthe_room')
    logo_url = serializers.SerializerMethodField(read_only=True, method_name='fetch_logo_url')
    class Meta:
        model = ChatRoomCommunity
        fields = [
            'id', 
            'owner', 
            'name', 
            'created', 
            'users_in_the_room', 
            'logo_url'
        ]
 
    def fetch_logo_url(self, obj):
        return obj.get_logo_url(self.context['request'])
    
    def get_users_inthe_room(self, obj):
        profiles = {'users':[]}
        users_qs = obj.get_users_in_the_room()

        for user in users_qs:
            profile = ProfileSerializer(
                user.profile, 
                context={'request':self.context['request']}
            )
            profiles['users'].append(profile.data)

        profiles['user_count'] = len(profiles['users'])
        
        return profiles
    

class CommunityMessageSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        model = CommunityMessage
        fields = ['id', 'community', 'author', 'message', 'created']


class UserMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    other_user = serializers.StringRelatedField()
    class Meta:
        model = UserMessage 
        fields = [
            'id', 
            'user', 
            'other_user', 
            'message', 
            'other_user_message', 
            'created',
            'other_meessage_created'
        ]


class ChatHistorySerializer(serializers.ModelSerializer):
    communities = serializers.SerializerMethodField(method_name='get_communities', read_only=True)
    users = serializers.SerializerMethodField(method_name='get_users', read_only=True)
    class Meta:
        model = ChatHistory
        fields = [
            'user', 
            'communities', 
            'users', 
        ]

    def get_communities(self, obj):
        community_list = []
        user = self.context['request'].user
        community_names = list(obj.communities.all().values_list('name', flat=True))

        for community in community_names:
            message = CommunityMessage.objects.filter(
                author=user, 
                community__name=community
            ).order_by('-created').select_related().first()

            if message:
                community_list.append({
                    'community':community, 
                    'last_chat_date':message.created,
                    'last_message':message.message,
                    'logo_url': message.community.get_logo_url(self.context['request'])
                })

        return community_list
    
    def get_users(self, obj):
        user_list = []
        user = self.context['request'].user
        users = list(obj.users.all().values_list('username', flat=True))

        for username in users:
            message = UserMessage.objects.filter(
                user=user, 
                other_user__username=username
            ).order_by('-created').select_related().first()

            if message:
                user_list.append({
                    'username':username, 
                    'last_chat_date':message.created,
                    'last_message':message.message,
                    'avatar_url': message.other_user.profile.get_avatar_url(self.context['request'])
                })

        return user_list

    
            