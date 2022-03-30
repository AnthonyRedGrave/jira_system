from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .models import Notification, Project
from .serializers import ProjectSerializer, NotificationSerializer
from .services import get_tasks_board


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["patch"])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        return Response(status=status.HTTP_200_OK)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset().filter(manager=self.request.user) | super().get_queryset().filter(developers__id__exact=self.request.user.id)
        return set(project for project in queryset)

    @action(detail=True, methods=["get"])
    def board(self, request, pk=None):
        project = self.get_object()
        tasks = get_tasks_board(project.tasks.all())
        return Response(tasks)