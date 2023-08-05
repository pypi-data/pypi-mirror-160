from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("", views.VersionViewSet, basename="version")

urlpatterns = router.urls
