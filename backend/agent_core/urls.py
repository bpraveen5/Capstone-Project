from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, CleaningJobViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'jobs', CleaningJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
