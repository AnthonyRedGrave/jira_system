from rest_framework import serializers
from rest_framework.validators import ValidationError

from django.contrib.auth.models import User

from django.db.models import Q

from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(many=False, source="user")
    chat = serializers.CharField()
    
    class Meta:
        model = Message
        fields = ('id', 'user', 'content', 'chat', 'user_name')
        read_only_fields = ('user', )

    def validate_chat(self, value):
        chat = Chat.objects.filter(id=value).last()
        if not chat:
            raise ValidationError("Такого чата не существует!")
        return chat


class ChatSerializer(serializers.ModelSerializer):
    member_1 = serializers.CharField()
    member_2 = serializers.CharField()

    class Meta:
        model = Chat
        fields = ('id', 'member_1', 'member_2')

    def validate(self, data):
        member_1 = data['member_1']
        member_2 = data['member_2']
        chat = Chat.objects.filter(Q(member_1=member_1, member_2 = member_2) | Q(member_1=member_2, member_2 = member_1)).last()
        if not chat:
            raise ValidationError("Такого чата не существует!")
        return data

    def validate_member_1(self, value):
        member_1 = User.objects.filter(Q(username__icontains=value) | Q(id__icontains = value)).last()
        if not member_1:
            raise ValidationError("Такого пользователя чата не существует!")
        return member_1

    def validate_member_2(self, value):
        member_2 = User.objects.filter(Q(username__icontains=value) | Q(id__icontains = value)).last()
        if not member_2:
            raise ValidationError("Такого пользователя чата не существует!")
        return member_2
