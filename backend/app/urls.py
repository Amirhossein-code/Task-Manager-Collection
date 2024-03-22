from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register("individual", views.IndividualViewSet, basename="individual")
router.register("tasks", views.TaskViewSet, basename="tasks")
router.register("categories", views.CategoryViewSet, basename="categories")

task_router = routers.NestedDefaultRouter(router, "tasks", lookup="task")
task_router.register(
    "prequisites", views.PrequisiteViewSet, basename="task-prerequisites"
)

urlpatterns = router.urls + task_router.urls
