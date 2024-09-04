from django.shortcuts import render

# Rest Framework
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


def home_view(request):
    return render(request, 'chat_room.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def messages_view(request):
    return Response(data={'message': 'New message'}, status=status.HTTP_200_OK)

