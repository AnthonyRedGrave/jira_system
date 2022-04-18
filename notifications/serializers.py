from rest_framework import serializers
from .models import Notification
from tasks.serializers import TaskSerializer


class NotificationSerializer(serializers.ModelSerializer):
    username_to = serializers.CharField(source="user")
    username_from = serializers.CharField(source="user_from")
    type_notification = serializers.CharField(source="get_type_display")
    project_title = serializers.CharField(source='project')
    task = TaskSerializer()

    class Meta:
        model = Notification
        fields = ("id", "project", "project_title", "username_to", "username_from", "type", "type_notification", "read", "message", "task")