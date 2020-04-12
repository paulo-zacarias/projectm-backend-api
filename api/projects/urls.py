from django.urls import include, path
from rest_framework import routers
from .views import ProjectViewSet, SprintViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]