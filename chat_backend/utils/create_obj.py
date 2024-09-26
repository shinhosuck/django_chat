from chat.models import (
    ChatRoomCommunity, 
    CommunityMessage,
    UserMessage,
    ChatHistory
)
from django.contrib.auth import get_user_model
from chat.serializers import (
    CommunityMessageSerializer, 
    UserMessageSerializer
)
from django.utils import timezone

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
    
    update_chat_history('community', user_obj, community)
    
    serializer = CommunityMessageSerializer(new_obj)

    return serializer.data


def create_private_message_obj(user, other_user, message, responding_to):
    try:
        user_obj = User.objects.get(username=user)
    except User.DoesNotExist:
        user_obj = None 
    try:
        recipient = User.objects.get(username=other_user)
    except User.DoesNotExist:
        recipient = None

    # if not response_to, other_user message instance gets created
    if not responding_to:
        instance = UserMessage.objects.create(
            user=recipient, 
            other_user=user_obj,
        )
        instance.other_user_message = message
        instance.other_meessage_created = timezone.now()
        instance.save()

    # user in reponding_to does not match user, then fetch the instance id in 
    # response_to and add the other_user_message
    if responding_to and responding_to['user'] != user:
        try:
            responding_to_obj = UserMessage.objects.get(id=responding_to['id'])
        except UserMessage.DoesNotExist:
            pass
        responding_to_obj.other_user_message = message
        responding_to_obj.other_meessage_created = timezone.now()
        responding_to_obj.save()
    
    # create user message instance
    new_instance = UserMessage.objects.create(
        user=user_obj, 
        other_user=recipient, 
        message=message,
    )

    update_chat_history('private', user_obj, recipient)

    serializer = UserMessageSerializer(new_instance)

    return serializer.data


def update_chat_history(community_or_user, user, other):
    instance, created = ChatHistory.objects.get_or_create(user=user)

    if community_or_user == 'private':
        if other in instance.users.all():
            instance.users.remove(other)
            instance.users.add(other)
        else:
            instance.users.add(other)

    elif community_or_user == 'community':
        if other in instance.communities.all():
            instance.communities.remove(other)
            instance.communities.add(other)
        else:
            instance.communities.add(other)

    return None