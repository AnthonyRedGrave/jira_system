from notifications.models import Notification
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import status
from .models import Project
from .serializers import CreateUpdateProjectSerializer, ProjectSerializer
from .services import get_tasks_board
from notifications.services import create_notification


class ProjectViewSet(mixins.UpdateModelMixin, mixins.CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUpdateProjectSerializer
        return super().get_serializer_class()


    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            project = Project.objects.create(title = serializer.validated_data['title'], type=serializer.validated_data['type'], manager = self.request.user)
            project.developers.set(serializer.validated_data['developers'])
            project.save()
            for dev in project.developers.all():
                create_notification(project, dev, project.manager, Notification.NotificationType.invitation)
            return Response(ProjectSerializer(project, context={'request': request}).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["post"])
    def add_developer(self, request, pk=None):
        project = self.get_object()
        serializer = CreateUpdateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        developer = serializer.validated_data['developers'][0]
        if developer not in project.developers.all():
            project.developers.add(developer)
        return Response('ASD')


    @action(detail=False, methods=["get"])
    def notifications(self, request, pk=None):
        projects = set(
            project
            for project in super().get_queryset().filter(manager=self.request.user)
            | super().get_queryset().filter(developers__id__exact=self.request.user.id)
            if project.num_notifications != 0
        )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def work(self, request, pk=None):
        projects = set(
            project
            for project in super().get_queryset().filter(manager=self.request.user)
            | super().get_queryset().filter(developers__id__exact=self.request.user.id)
        )
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def board(self, request, pk=None):
        project = self.get_object()
        tasks = get_tasks_board(project.tasks.all())
        return Response(tasks)
