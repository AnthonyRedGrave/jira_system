from tasks.serializers import PartialUpdateTaskSerializer, TaskSerializer, TypeTaskSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Task, TypeTask, EpicTask
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins


class TaskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PartialUpdateTaskSerializer
        return super().get_serializer_class()

    
    def perform_update(self, serializer):
        task = self.get_object()
        print(serializer.validated_data)
        task.title = serializer.validated_data.get('title', task.title)
        task.description = serializer.validated_data.get('description', task.description)
        task.type_task = serializer.validated_data.get('type_task', task.type_task)
        task.epic_task = serializer.validated_data.get('epic_task', task.epic_task)
        task.implementer = serializer.validated_data.get('implementer', task.implementer)
        task.save()
        return Response(serializer.data)
    


class TypeTaskViewSet(ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    queryset = TypeTask.objects.all()
    serializer_class = TypeTaskSerializer

    