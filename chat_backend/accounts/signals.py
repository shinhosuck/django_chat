from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.authtoken.models import Token

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.email = instance.email
        profile.save()

@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)