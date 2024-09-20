from rest_framework_nested import routers

from .views import IndividualViewSet

# Define the namespace
app_name = "individual"

router = routers.DefaultRouter()

router.register("individual", IndividualViewSet, basename="individual")

urlpatterns = router.urls
