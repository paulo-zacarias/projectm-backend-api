from django.urls import include, path
from rest_framework import routers
from .views import ProjectViewSet, SprintViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
# router.register(r'sprints', SprintViewSet)  # 'basename' allows the queryset to be override in view
router.register(r'sprints', SprintViewSet, basename='sprints')  # 'basename' allows the queryset to be override in view
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]