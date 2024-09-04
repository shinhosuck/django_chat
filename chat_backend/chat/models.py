from django.db import models
from django.conf import settings 


User = settings.AUTH_USER_MODEL


class ChatRoomName(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
    

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoomName, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}\'s message'