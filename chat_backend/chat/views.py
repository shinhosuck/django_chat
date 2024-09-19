from django.shortcuts import render
from .models import (
    ChatRoomCommunity, 
    CommunityMessage, 
    UserMessage,
    ChatHistory
)
from .serializers import (
    CommunityMessageSerializer, 
    ChatRoomCommunitySerializer,
    ChatHitorySerializer,
    UserMessageSerializer
)

# Rest Framework
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.parsers import (
    FormParser, 
    MultiPartParser
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes
)


class ChatRoomCommunityView(ListAPIView):
    serializer_class = ChatRoomCommunitySerializer
    permission_classes = [AllowAny]
    queryset = ChatRoomCommunity.objects\
        .prefetch_related('messages').all()
    

class CommunityMessagesView(ListAPIView):
    queryset = CommunityMessage.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset =  self.get_queryset().filter(community__name=kwargs['community_name'])
        serializer = CommunityMessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMessagesView(ListAPIView):
    queryset = UserMessage.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user__username=kwargs['username'])
        serializer = UserMessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChatHistoryView(ListAPIView):
    queryset = ChatHistory.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(user=request.user).first()
        serializer = ChatHitorySerializer(obj)
        return Response(serializer.data)


