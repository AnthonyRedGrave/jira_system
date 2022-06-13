
from django.db.models.query_utils import Q

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.decorators import action

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, CreateChatSerializer


class MessageViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat = serializer.validated_data['chat']
        user = self.request.user

        if user != chat.member_1 and user != chat.member_2:
            raise APIException("Чтобы отправлять сообщения в чат пользователь должен быть его участником!")
        Message.objects.create(**serializer.validated_data, user = self.request.user)
        

class ChatViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(Q(member_1 = self.request.user) | Q(member_2 = self.request.user))

    def get_serializer_class(self):
        if self.action == "create":
            return CreateChatSerializer
        return super().get_serializer_class()

    @action(detail=True, methods = ['get', 'post'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        if request.method == "GET":
            serializer = MessageSerializer(chat.get_messages(), many=True)
            return Response(serializer.data)
        else:
            data = {
                "content": request.data['content'],
                "chat": chat.id
            }
            serializer = MessageSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            Message.objects.create(**serializer.validated_data, user=request.user)
            return Response({"Message": "Created!"})


    def perform_create(self, serializer):
        Chat.objects.create(**serializer.validated_data)