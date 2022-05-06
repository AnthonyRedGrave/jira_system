from tasks.serializers import (
    CreatePartialUpdateTaskSerializer,
    TaskSerializer,
    TypeTaskSerializer,
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Task, TypeTask
from notifications.models import Notification
from notifications.services import create_notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins


class TaskViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, ReadOnlyModelViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "create":
            return CreatePartialUpdateTaskSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset().filter(implementer=self.request.user)
        return queryset

    def perform_create(self, serializer):
        if serializer.validated_data.get("implementer"):
            new_task = Task.objects.create(**serializer.validated_data)
            create_notification(
                new_task.project, self.request.user, new_task.project.manager, Notification.NotificationType.task
            )
        else:
            new_task = Task.objects.create(
                implementer=self.request.user, **serializer.validated_data
            )
            create_notification(
                new_task.project,
                new_task.project.manager,
                self.request.user,
                Notification.NotificationType.message,
            )
        return new_task

    def perform_update(self, serializer):
        task = self.get_object()
        task.title = serializer.validated_data.get("title", task.title)
        task.description = serializer.validated_data.get(
            "description", task.description
        )
        task.type_task = serializer.validated_data.get("type_task", task.type_task)
        task.epic_task = serializer.validated_data.get("epic_task", task.epic_task)
        task.implementer = serializer.validated_data.get(
            "implementer", task.implementer
        )
        task.save()
        if serializer.validated_data.get("implementer"):
            create_notification(
                task.project,
                task.implementer,
                Notification.NotificationType.change.value,
            )
        else:
            create_notification(
                task.project,
                task.project.manager,
                Notification.NotificationType.message,
            )
        return Response(serializer.data)


class TypeTaskViewSet(ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    queryset = TypeTask.objects.all()
    serializer_class = TypeTaskSerializer
