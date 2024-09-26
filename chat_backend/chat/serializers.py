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
    # messages = serializers.SerializerMethodField(read_only=True, method_name='get_messages')
    logo_url = serializers.SerializerMethodField(read_only=True, method_name='fetch_logo_url')
    class Meta:
        model = ChatRoomCommunity
        fields = ['id', 'owner', 'name', 'created', 'messages', 'logo_url']

    # def get_messages(self, obj):
    #     serializer =CommunityMessageSerializer(obj.messages.all(), many=True)
    #     return serializer.data
    
    def fetch_logo_url(self, obj):
        return obj.get_logo_url(self.context['request'])
    

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
        community_list = []
        user = self.context['request'].user
        communities = list(obj.communities.all().values_list('name', flat=True))

        # for community in communities:
        #     message = CommunityMessage.objects.filter(
        #         author=user, 
        #         community__name=community
        #     ).order_by('-created').select_related().first()

        #     if message:
        #         communities_list.append({
        #             'community':community, 
        #             'last_chat_date':message.created,
        #             'logo_url': message.community.get_logo_url(self.context['request'])
        #         })
        # print(community_list)
        return communities
    
    def get_last_chat_date_community(self, obj):
        user = self.context.get('request').user
        communities = self.get_communities(obj)
        last_chat_dates = {}

        for community in communities:
            messages = CommunityMessage.objects.filter(author=user, community__name=community)\
            .order_by('-created')

            if messages:
                last_chat_dates[community] = str(messages.first().created)
              
        return last_chat_dates

    def get_users(self, obj):
        user_list = []
        user = self.context['request'].user
        users = list(obj.users.all().values_list('username', flat=True))

        # for username in users:
        #     message = UserMessage.objects.filter(
        #         user=user, 
        #         other_user__username=username
        #     ).order_by('-created').select_related().first()

        #     if message:
        #         user_list.append({
        #             'username':username, 
        #             'last_chat_date':message.created,
        #             'avatar_url': message.other_user.profile.get_avatar_url(self.context['request'])
        #         })
        # print(user_list)

        return users

    def get_last_chat_users(self, obj):
        user = self.context.get('request').user
        users = self.get_users(obj)

        last_chat_dates = {}

        for username in users:
            user_obj = User.objects.get(username=username)

            messages = UserMessage.objects.filter(user=user, other_user=user_obj)\
            .order_by('-created')

            avatar_url = user_obj.profile.get_avatar_url(self.context['request'])

            if messages:
                last_chat_dates[username] = str(messages.first().created)
                last_chat_dates["avatar_url"] = avatar_url
                
        return last_chat_dates
            