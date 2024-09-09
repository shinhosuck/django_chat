from django.shortcuts import render, get_object_or_404
from .serializers import (
    UserRegisterSerializer, 
    UpdateUserProfileSerializer,
    ProfileSerializer
)
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
)

# Rest Framework
from rest_framework.decorators import (
    api_view, 
    permission_classes, 
    authentication_classes,
    parser_classes
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.parsers import (
    MultiPartParser, FormParser
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

# Custom error handler
from utils.error_handlers import (
    handle_error_response
)

# Custom permissions
from utils.permissions import (
    CanAccessUserProfiles, 
    IsActiveUser
)

User = get_user_model()

@api_view(['GET'])
def get_profiles_view(request):
    if request.user.is_staff:
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Not allowed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_view(request):
    data = request.data 
    serializer =  UserRegisterSerializer(data=data, context={'request':request})
    if serializer.is_valid():
        serializer.save()
        return Response({**serializer.data,'message': 'successfully registered'},
                status=status.HTTP_201_CREATED)
    errors = handle_error_response(serializer)
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error':"Password or username did not match."}, 
                        status=status.HTTP_400_BAD_REQUEST)
    is_valid = user.check_password(password)
    if is_valid:
        serializer = ProfileSerializer(user.profile, context={'request':request})
        return Response({**serializer.data, 'message':'Successfully logged in.'}, status=status.HTTP_200_OK)
    return Response({'error':'Password or username did not match.'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
# @parser_classes([FormParser, MultiPartParser])
def update_profile_view(request):
    user = request.user
    try:
        user = User.objects.get(id=user.id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UpdateUserProfileSerializer(user.profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({**serializer.data, 'message': 'success'}, status=status.HTTP_200_OK)
    errors = handle_error_response(serializer)
    return Response(errors)


@api_view(['POST'])
def validate_username_email(request):
    username = request.data.get('username')
    email = request.data.get('email')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    try:
        email_user = User.objects.get(email=email)
    except User.DoesNotExist:
        email_user = None 
    
    if not user and not email_user:
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

    obj = {
        'user':user and 'This username is taken.' or None, 
        'email':email_user and 'This email is taken.' or None
    }
    return Response({'user_exists':{**obj}}, status=status.HTTP_400_BAD_REQUEST)

