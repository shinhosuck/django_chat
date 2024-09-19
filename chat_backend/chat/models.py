from django.db import models
from django.conf import settings 


User = settings.AUTH_USER_MODEL


class ChatRoomCommunity(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Chat Room Communities'

    def __str__(self):
        return self.name 
    

class CommunityMessage(models.Model):
    community = models.ForeignKey(ChatRoomCommunity, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}\'s message'
    

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'
    

class ChatHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_history')
    communities = models.ManyToManyField(ChatRoomCommunity)
    users = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = 'Chat History'

    def __str__(self):
        return f'{self.user.username}'
