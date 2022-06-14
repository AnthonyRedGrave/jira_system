from rest_framework.validators import ValidationError
from tasks.serializers import RoadMapTaskSerializer, TaskSerializer
from notifications.serializers import NotificationSerializer
from tasks.models import Task
from rest_framework import serializers
from .models import Project, RoadMap
from notifications.models import Notification
from django.contrib.auth import get_user_model
import datetime


User = get_user_model()


class ProfileProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.StringRelatedField(source="manager")
    type = serializers.ChoiceField(
        choices=Project.TypeProject, source="get_type_display"
    )
    tasks = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "manager_name",
            "type",
            "tasks"
        )
    def get_tasks(self, obj):
        return obj.tasks.count()


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


class RoadMapSerializer(serializers.ModelSerializer):
    project = ProfileProjectSerializer()
    roadmaptasks = RoadMapTaskSerializer(many=True)
    class Meta:
        model = RoadMap
        fields = '__all__'


class CreateUpdateProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title=serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=Project.TypeProject, required=False)
    developers = serializers.CharField(required=False)
    deadline = serializers.CharField(required=False)

    def validate_deadline(self, value):
        if datetime.date(*[int(i) for i in value.split('.')][::-1]) < datetime.date.today():
            raise ValidationError({'Дедлайн': 'Неправильная дата'})
        return value

    def validate_title(self, value):
        projects = Project.objects.filter(title = value).last()
        if projects:
            raise ValidationError({"Название": "Проект с таким именем уже существует!"})
        return value

    def validate_developers(self, value):
        developers = value.split(",")
        developers_db = User.objects.filter(username__in=developers).all()
        if len(developers) != len(developers_db):
            raise ValidationError({"Разработчики": "Не все пользователи существуют!"})
        return list(developers_db)
