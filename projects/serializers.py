from tasks.serializers import TaskSerializer
from tasks.models import Task
from rest_framework import serializers
from .models import Project, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'project', 'user', 'type', 'read')


class ProjectSerializer(serializers.ModelSerializer):

    manager_name = serializers.StringRelatedField(source="manager")
    type = serializers.ChoiceField(
        choices=Project.TypeProject, source="get_type_display"
    )
    developers = serializers.StringRelatedField(many=True)
    notifications = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()

    def get_notifications(self, obj):
        return (
            Notification.objects.filter(user=self.context["request"].user, project=obj)
            .exclude(type=Notification.NotificationType.invitation.value)
            .count()
        )
    
    def get_last_task(self, obj):
        last_task = Task.objects.filter(implementer=self.context["request"].user, project=obj).last()
        if last_task:
            return TaskSerializer(last_task).data
        return {}

    class Meta:
        model = Project
        fields = ("id", "title", "manager_name", "type", "developers", "notifications", "last_task")
