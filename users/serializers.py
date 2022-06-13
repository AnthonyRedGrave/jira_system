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


class ProfileSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    tools = ToolSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'last_login', 'image', 'projects', 'tools')

    def get_projects(self, obj):
        projects = Project.objects.filter(developers__id__exact = obj.id)
        # print(projects)
        serializer = ProfileProjectSerializer(projects, many=True)
        return serializer.data