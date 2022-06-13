from users.serializers import UserSerializer, ProfileSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        username = self.request.query_params.get('username')
        queryset = super().get_queryset()
        if username:
            return queryset.filter(username__istartswith=username).exclude(id=self.request.user.id)
        return queryset

    @action(detail=False, methods=["get"])
    def profile(self, request, pk=None):
        profile = request.user
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)