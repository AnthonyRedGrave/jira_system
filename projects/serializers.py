from rest_framework.validators import ValidationError
from tasks.serializers import TaskSerializer
from notifications.serializers import NotificationSerializer
from tasks.models import Task
from rest_framework import serializers
from .models import Project
from notifications.models import Notification
from django.contrib.auth import get_user_model


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):

    manager_name = serializers.StringRelatedField(source="manager")
    type = serializers.ChoiceField(
        choices=Project.TypeProject, source="get_type_display"
    )
    developers = serializers.StringRelatedField(many=True)
    notifications = serializers.SerializerMethodField()
    last_task = serializers.SerializerMethodField()

    def get_notifications(self, obj):
        notifications = Notification.objects.filter(
            user=self.context["request"].user, project=obj, read=False
        )
        return NotificationSerializer(notifications, many=True).data

    def get_last_task(self, obj):
        last_task = Task.objects.filter(
            implementer=self.context["request"].user, project=obj
        ).last()
        if last_task:
            return TaskSerializer(last_task).data
        return {}

    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "manager_name",
            "type",
            "developers",
            "notifications",
            "last_task",
        )



class CreateUpdateProjectSerializer(serializers.Serializer):
    title=serializers.CharField()
    type = serializers.ChoiceField(choices=Project.TypeProject)
    developers = serializers.CharField()

    def validate_developers(self, value):
        developers = value.split(",")
        developers_db = User.objects.filter(username__in=developers).all()
        if len(developers) != len(developers_db):
            raise ValidationError("Не все пользователи существуют!")
        return list(developers_db)
