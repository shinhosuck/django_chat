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
    ChatHistorySerializer,
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
        if serializer.data:
            return Response({
                'message_list': serializer.data, 'type':'community'},
                status=status.HTTP_200_OK
            )
        return Response({
            'message': 'Messages available'}, 
            status=status.HTTP_200_OK
        )


class UserMessagesView(ListAPIView):
    queryset = UserMessage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            user=request.user,
            other_user__username=kwargs['username']
        )

        serializer = UserMessageSerializer(queryset, many=True)
       
        if serializer.data:
            return Response({
                'messages_list':serializer.data, 'type':'user'},
                status=status.HTTP_200_OK
            )
        return Response({
            'message': 'Messages not available'}, 
            status=status.HTTP_200_OK
        )
    
class ChatHistoryView(RetrieveAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        qs = queryset.filter(user__username=kwargs['username']).first()

        data = self.get_serializer(qs, context={'request':request}).data
        
        if not data['user']:
            return Response(
                {'message':'You do not have a chat history yet.'}, 
                status=status.HTTP_200_OK
            )
        return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_community_room(request):
    rooms = ChatRoomCommunity.objects.all()
    data = request.data 

    if not 'previousRoom' in data:
        room = rooms.get(name=data.get('currentRoom'))
        room.users_in_the_room.add(request.user)

    elif 'previousRoom' in data:
        previous_room = rooms.get(name=data.get('previousRoom'))
        previous_room.users_in_the_room.remove(request.user)

        current_room = rooms.get(name=data.get('currentRoom'))
        current_room.users_in_the_room.add(request.user)
    
    return Response({'message':'Success'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_community_chat_session(request, username):
    user = request.user 

    if user.username == username:
        communities = ChatRoomCommunity.objects.filter(
            users_in_the_room=user
        )
        
        if communities:
            for room in communities:
                room.users_in_the_room.remove(user)

        return Response({'message': 'success'}, status=status.HTTP_200_OK)
    
    return Response(
            {'error':'Username or password did not match.'},
            status=status.HTTP_400_BAD_REQUEST
        )