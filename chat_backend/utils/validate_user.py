from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_community_chat_user(user):
    username = user.get('user')
    token = user.get('token')

    if not username or username == 'undefined' or not token or token == 'undefined':
        return {'error':'You must login to chat.'}
    
    try:
        token_obj = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return {'error':'User does not exist.'}
    
    valid = token_obj.user.username == username or False

    return {'valid':valid}


def get_current_user(query_string):
    current_user = {}

    for string in query_string.decode().split('&'):
        key, value = string.split('=')
        if key == 'user':
            current_user['user'] = value 
        else:
            current_user['token'] = value

    return current_user


def validate_private_chat_users(user, other_user):
    validate_obj = {}
    username = user.get('user')
    token = user.get('token')

    if not username or username == 'undefined' or not token or token == 'undefined':
        validate_obj['error'] = 'You must login to chat.'
        return validate_obj
    
    try:
        token_obj = Token.objects.get(key=token)
    except Token.DoesNotExist:
        validate_obj['error'] = 'User does not exist.'
        return validate_obj
    
    try:
        other_user_obj = User.objects.get(username=other_user)
    except User.DoesNotExist:
        validate_obj['error'] = 'Chat recipient does not exist'
        return validate_obj

    if not token_obj.user.username == username:
        validate_obj['error'] = 'Username or password did not match'
        return validate_obj
    else:
        validate_obj['other_user_id'] = other_user_obj.id
        private_chat_room = ''.join([str(num) for num in sorted([int(other_user_obj.id),int(token_obj.user.id)])])
        validate_obj['private_chat_room'] = f'chat_room_{private_chat_room}'
    
    return validate_obj