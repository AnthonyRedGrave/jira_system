from tasks.serializers import TaskSerializer, TypeTaskSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Task, TypeTask, EpicTask
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TypeTaskViewSet(ModelViewSet):
    queryset = TypeTask.objects.all()
    serializer_class = TypeTaskSerializer

    @action(detail=False, methods=['GET'])
    def tasks(self, request):
        serializer = TypeTaskSerializer(Task.objects.all(), many=True)
        return Response(serializer.data)