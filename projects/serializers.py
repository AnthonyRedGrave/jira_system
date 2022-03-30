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

    def get_notifications(self, obj):
        return (
            Notification.objects.filter(user=self.context["request"].user, project=obj)
            .exclude(type=Notification.NotificationType.invitation.value)
            .count()
        )

    class Meta:
        model = Project
        fields = ("id", "title", "manager_name", "type", "developers", "notifications")
