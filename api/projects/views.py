from .models import Project, Sprint, Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer
from .permissions import IsAdminOrReadOnly, IsProjectParticipant


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        # Define the logged in user as admin directly, rather than from request data.
        serializer.save(admin=self.request.user)


class SprintViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sprints to be viewed or edited.
    """
    serializer_class = SprintSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given project,
        by filtering against a `project` query parameter in the URL.
        Accessible through URL: /sprints/?project='project_id'
        """
        queryset = Sprint.objects.all()
        project = self.request.query_params.get('project_id', None)
        if project is not None:
            queryset = queryset.filter(project=project)
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectParticipant]