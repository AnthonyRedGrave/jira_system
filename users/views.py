from users.serializers import UserSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
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
            print(queryset.filter(username__istartswith=username).exclude(id=self.request.user.id))
            return queryset.filter(username__istartswith=username).exclude(id=self.request.user.id)
        return queryset
