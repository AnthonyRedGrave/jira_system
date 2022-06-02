from users.views import UserViewSet
from rest_framework.routers import SimpleRouter
from .views import EpicTaskViewSet, TaskViewSet, TypeTaskViewSet
from projects.views import ProjectViewSet
from notifications.views import NotificationViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('types', TypeTaskViewSet)
router.register('epics', EpicTaskViewSet)
router.register('projects', ProjectViewSet)
router.register('notifications', NotificationViewSet)
router.register('users', UserViewSet)


urlpatterns = router.urls
