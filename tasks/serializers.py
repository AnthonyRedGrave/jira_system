from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import Task, TypeTask, EpicTask
from projects.serializers import ProjectSerializer
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(source="type_task")
    epic = serializers.StringRelatedField(source="epic_task")
    developer = serializers.StringRelatedField(source="implementer")
    project = ProjectSerializer()


    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'epic', 'developer', 'project')



class PartialUpdateTaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    type_task = serializers.CharField()
    epic_task = serializers.CharField()
    implementer = serializers.CharField()

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


    


    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     return super().update(instance, validated_data)



class TypeTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = TypeTask
        fields = ('id', 'title', 'tasks')
