from logging.config import valid_ident
from django.forms import ValidationError
from rest_framework import serializers
from projects.models import Project
from projects.serializers import ProfileProjectSerializer
from django.contrib.auth import get_user_model

from users.models import Tool

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'last_login', 'image')


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ('id', 'title')

    def validate_title(self, value):
        tool = Tool.objects.filter(title=value).last()
        if tool:
            raise ValidationError("Такой инструмент уже существует!")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tools = ToolSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'last_login', 'image', 'projects', 'tools', 'position')

    def get_projects(self, obj):
        projects = Project.objects.filter(developers__id__exact = obj.id)
        # print(projects)
        serializer = ProfileProjectSerializer(projects, many=True)
        return serializer.data