from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from .services import get_tasks_board


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    @action(detail=True, methods=["get"])
    def board(self, request, pk=None):
        project = self.get_object()
        tasks = get_tasks_board(project.tasks.all())
        return Response(tasks)