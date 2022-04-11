from rest_framework.routers import SimpleRouter
from .views import TaskViewSet, TypeTaskViewSet
from projects.views import ProjectViewSet
from notifications.views import NotificationViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('types', TypeTaskViewSet)
router.register('projects', ProjectViewSet)
router.register('notifications', NotificationViewSet)


urlpatterns = router.urls
