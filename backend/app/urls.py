from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("tasks", views.TaskViewSet, basename="tasks")


urlpatterns = router.urls
