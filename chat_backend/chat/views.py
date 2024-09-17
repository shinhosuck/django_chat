from django.shortcuts import render
from .models import ChatRoomName, Message
from .serializers import MessageSerializer, ChatRoomNameSerializer

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


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def chat_room_names_view(request):
#     qs = ChatRoomName.objects \
#         .prefetch_related('messages') \
#         .select_related('owner').all()
#     serializer = ChatRoomNameSerializer(qs, many=True)
#     return Response(data=serializer.data, status=status.HTTP_200_OK)

class ChatRoomNamesView(ListAPIView):
    serializer_class = ChatRoomNameSerializer
    permission_classes = [AllowAny]
    queryset = ChatRoomName.objects\
        .prefetch_related('messages').all()
    
    # def list(self, request, *args, **kwargs):
    #     serializer_roomname = ChatRoomNameSerializer(self.get_queryset(), many=True)
    #     for data in serializer_roomname.data:
    #         messages = self.get_queryset().get(id=data['id']).messages.all()
    #         data['messages'] = MessageSerializer(messages, many=True).data
    #     return Response(serializer_roomname.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def messages_view(request):
    qs = Message.objects.all() \
        .select_related('author') \
        .select_related('chat_room')
    
    serializer = MessageSerializer(qs, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

