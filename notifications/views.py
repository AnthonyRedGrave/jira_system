from rest_framework.viewsets import ModelViewSet
from notifications.serializers import NotificationSerializer
from notifications.models import Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        type = self.request.query_params.get('type')
        queryset = super().get_queryset().filter(user=self.request.user)
        if type:
            queryset = queryset.filter(type=type)
        return queryset

    @action(detail=True, methods=["patch"])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        return Response(status=status.HTTP_200_OK)
