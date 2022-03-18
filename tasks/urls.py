from rest_framework.routers import SimpleRouter
from .views import TaskViewSet, TypeTaskViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet)
router.register('types', TypeTaskViewSet)


urlpatterns = router.urls
