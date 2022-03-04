from rest_framework import serializers
from .models import Task, TypeTask, EpicTask


class TaskSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField(source="type_task")
    epic = serializers.StringRelatedField(source="epic_task")
    developer = serializers.StringRelatedField(source="implementer")

    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'epic', 'developer')



class TypeTaskSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    class Meta:
        model = TypeTask
        fields = ('id', 'title', 'tasks')