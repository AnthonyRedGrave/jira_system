from users.views import UserViewSet, ToolViewSet
from rest_framework.routers import SimpleRouter
from .views import EpicTaskViewSet, TaskViewSet, TypeTaskViewSet, RoadMapTaskViewSet
from projects.views import ProjectViewSet, RoadMapViewSet
from notifications.views import NotificationViewSet
from chats.views import ChatViewSet, MessageViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('types', TypeTaskViewSet)
router.register('epics', EpicTaskViewSet)
router.register('projects', ProjectViewSet)
router.register('notifications', NotificationViewSet)
router.register('users', UserViewSet)
router.register('chats', ChatViewSet)
router.register('messages', MessageViewSet)
router.register('tools', ToolViewSet)
router.register('roadmaps', RoadMapViewSet)
router.register('roadmap_tasks', RoadMapTaskViewSet)


urlpatterns = router.urls
