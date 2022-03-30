from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer
from .services import get_tasks_board


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