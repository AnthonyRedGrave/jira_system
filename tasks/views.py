from pkg_resources import require
from tasks.serializers import (
    CreatePartialUpdateTaskSerializer,
    CreateTypeTaskSerializer,
    TaskSerializer,
    TypeTaskSerializer,
    EpicTaskSerializer,
    CreateEpicTaskSerializer,
    RoadMapTaskSerializer
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import EpicTask, RoadMapTask, Task, TypeTask
from notifications.models import Notification
from notifications.services import create_notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from projects.services import get_tasks_board
from .services import create_road_map_task


class RoadMapTaskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, ReadOnlyModelViewSet):
    queryset = RoadMapTask.objects.all()
    serializer_class = RoadMapTaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, ReadOnlyModelViewSet
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

    @action(detail=False, methods=["get"])
    def filter_tasks(self, request):
        developer = request.query_params.get('developer')
        project = request.query_params.get('project')
        epic = request.query_params.get('epic')
        if epic:
            tasks = get_tasks_board(super().get_queryset().filter(epic_task__title = epic))
        elif developer:
            tasks = get_tasks_board(super().get_queryset().filter(implementer__username=developer, project = project))
        return Response(tasks)


    def perform_create(self, serializer):
        if serializer.validated_data.get("implementer"):
            new_task = Task.objects.create(**serializer.validated_data)
            create_notification(
                new_task.project, serializer.validated_data.get("implementer"), new_task.project.manager, Notification.NotificationType.task
            )
            content = f'{serializer.validated_data.get("implementer")} добавил задачу {new_task.title}'
        else:

            new_task = Task.objects.create(
                implementer=self.request.user, **serializer.validated_data
            )
            if self.request.user != new_task.project.manager:
                create_notification(
                    new_task.project,
                    self.request.user,
                    new_task.project.manager,
                    Notification.NotificationType.message,
                )
            
            content = f'{self.request.user} добавил задачу {new_task.title}'
        roadmap = new_task.project.roadmap
        create_road_map_task(new_task, content, roadmap)
        return new_task

    def perform_update(self, serializer):
        task = self.get_object()
        task.title = serializer.validated_data.get("title", task.title)
        task.description = serializer.validated_data.get(
            "description", task.description
        )
        message_value = "Редактирование задачи"

        if serializer.validated_data.get("type_task"):
            message_value = f"{task.type_task} => {serializer.validated_data['type_task']}"
            task.type_task = serializer.validated_data['type_task']
            
        else:
            task.type_task = task.type_task

        task.epic_task = serializer.validated_data.get("epic_task", task.epic_task)
        task.implementer = serializer.validated_data.get(
            "implementer", task.implementer
        )
        task.save()
        
        if serializer.validated_data.get("implementer"):
            
            create_notification(
                task.project,
                task.project.manager,
                serializer.validated_data.get("implementer"),
                Notification.NotificationType.change.value,
                message_value
            )
        else:
            if self.request.user != task.project.manager:
                create_notification(
                    task.project,
                    self.request.user,
                    task.project.manager,
                    Notification.NotificationType.change.value,
                    message_value
                )
        roadmap = task.project.roadmap
        create_road_map_task(task, message_value, roadmap)
        return Response(serializer.data)


class TypeTaskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = TypeTask.objects.all()
    serializer_class = TypeTaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTypeTaskSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        TypeTask.objects.create(title=serializer.validated_data['title'])
        
        return Response("Created!")

class EpicTaskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = EpicTask.objects.all()
    serializer_class = EpicTaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEpicTaskSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        EpicTask.objects.create(title=serializer.validated_data['title'])
        return Response("Created!")