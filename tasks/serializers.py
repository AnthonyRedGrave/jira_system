from projects.models import Project
from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import Task, TypeTask, EpicTask
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(source="type_task")
    epic = serializers.StringRelatedField(source="epic_task")
    epic_color = serializers.StringRelatedField(source="epic_task.color")
    developer = serializers.StringRelatedField(source="implementer")


    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'epic', 'description', 'developer', 'project', 'epic_color')



class CreatePartialUpdateTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    type_task = serializers.CharField()
    epic_task = serializers.CharField()
    description = serializers.CharField()
    implementer = serializers.CharField(required=False)
    project = serializers.CharField()

    def validate_type_task(self, value):
        type_task = TypeTask.objects.filter(title=value).last()
        if not type_task:
            raise ValidationError("Такого типа задачи не существует!")
        return type_task

    def validate_epic_task(self, value):
        epic_task = EpicTask.objects.filter(title=value).last()
        if not epic_task:
            raise ValidationError("Такого епика для задачи не существует!")
        return epic_task

    def validate_implementer(self, value):
        implementer = User.objects.filter(username=value).last()
        if not implementer:
            raise ValidationError("Такого разработчика не существует!")
        return implementer

    def validate_project(self, value):
        project = Project.objects.filter(id=value).last()
        if not project:
            raise ValidationError("Такого проекта не существует!")
        return project


class TypeTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = TypeTask
        fields = ('id', 'title', 'tasks')


class CreateTypeTaskSerializer(serializers.Serializer):
    title = serializers.CharField()

    def validate_title(self, value):
        if TypeTask.objects.filter(title=value).first():
            raise ValidationError("Тип для задач с таким названием уже существует!")
        return value


class EpicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpicTask
        fields = ('id', 'title', 'color')


class CreateEpicTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    color = serializers.CharField()

    def validate_title(self, value):
        if EpicTask.objects.filter(title=value).first():
            raise ValidationError("Тип для задач с таким названием уже существует!")
        return value