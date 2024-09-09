from typing import Iterable
from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
            upload_to='avatars',
            default='avatars/default.png',
            null=True, blank=True
        )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'
    
    @property
    def get_user_token(self):
        obj, created = Token.objects.get_or_create(user=self.user)
        return obj.key
    
    def get_avatar_url(self, request):
        img_path = self.avatar.url
        return request.build_absolute_uri(img_path)
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatars/default.png'
        return super().save(*args, **kwargs)