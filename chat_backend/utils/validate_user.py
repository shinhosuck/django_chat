from rest_framework.authtoken.models import Token

def validate_user(user):
    username = user.get('user')
    token = user.get('token')

    if not username or username == 'undefined' or not token or token == 'undefined':
        return {'error':'You must login to chat.'}
    
    try:
        token_obj = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return {'error':'User does not exist.'}
    
    valid = token_obj.user.username == username or False
    
    return valid and {'valid': valid} or {'error':'User name or password did not match.'}