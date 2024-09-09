from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.forms import model_to_dict
from .models import Profile

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        return validated_data


        
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    class Meta:
        model = Profile 
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'avatar', 
            'email'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance.avatar = validated_data.get('avatar')
        instance.save()

        if validated_data.get('username'):
            if instance.user.username != validated_data.get('username'):
                instance.user.username = validated_data.get('username')
                instance.user.save()
        return validated_data
    

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    token = serializers.SerializerMethodField(method_name='get_token', read_only=True)
    avatar_url = serializers.SerializerMethodField(method_name='get_avatar_url', read_only=True)
    user_id = serializers.SerializerMethodField(method_name='get_user_id', read_only=True)
    class Meta:
        model = Profile 
        fields = [
                'id', 
                'user', 
                'user_id',
                # 'avatar',  
                'first_name', 
                'last_name', 
                'email', 
                'token', 
                'avatar_url',
            ]

    def get_user_id(self, obj):
        return obj.user.id

    def get_token(self, obj):
        return obj.get_user_token

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        return obj.get_avatar_url(request)
    
    

