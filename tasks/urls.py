from rest_framework.routers import SimpleRouter
from .views import TaskViewSet, TypeTaskViewSet
from projects.views import ProjectViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('types', TypeTaskViewSet)
router.register('projects', ProjectViewSet)


urlpatterns = router.urls
