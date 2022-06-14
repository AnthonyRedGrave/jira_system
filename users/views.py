from users.models import Tool
from users.serializers import ToolSerializer, UserSerializer, ProfileSerializer, CreateUserSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from django.contrib.auth import authenticate


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

   
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request, pk=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User(username = serializer.validated_data['username'], 
            first_name=serializer.validated_data['first_name'], 
            last_name = serializer.validated_data['last_name'])
            user.save()
            user.set_password(request.data['password'])
            user.save()
            if not user:
                return Response('Error!')
        return Response('Created!')

    @action(detail=True, methods=["get"])
    def other_profile(self, request, pk=None):
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ToolViewSet(CreateModelMixin, UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):        
        tool = Tool.objects.create(**serializer.validated_data)
        self.request.user.tools.add(tool)
        return 'Created!'

    