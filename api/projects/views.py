from .models import Project, Sprint, Task
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Define the logged in user as admin directly, rather than from request data.
        serializer.save(admin=self.request.user)


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sprints to be viewed or edited.
    """
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]