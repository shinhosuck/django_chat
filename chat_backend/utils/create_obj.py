from chat.models import (
    ChatRoomCommunity, 
    CommunityMessage,
    UserMessage,
    ChatHistory
)
from django.contrib.auth import get_user_model
from chat.serializers import CommunityMessageSerializer


User = get_user_model()


def create_community_message_obj(user, message):
    try:
        user_obj = User.objects.get(username=user['user'])
    except User.DoesNotExist:
        return False
    try:
        community = ChatRoomCommunity.objects.get(name=message['community'])
    except ChatRoomCommunity.DoesNotExist:
        return False
    
    new_obj = CommunityMessage.objects.create(
            community = community,
            author = user_obj,
            message = message['message']
        )

    instance, created = ChatHistory.objects.get_or_create(user=user_obj)

    if  community in instance.communities.all():
        instance.communities.remove(community)
        instance.communities.add(community)
    else:
        instance.communities.add(community)

    instance.save()
    
    serializer = CommunityMessageSerializer(new_obj)
    return serializer.data