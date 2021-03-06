from .models import Project, Sprint, Task
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer
from .permissions import IsProjectAdminOrReadOnly, IsProjectParticipant


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsProjectAdminOrReadOnly]

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
        queryset = Sprint.objects.all().order_by('-end_date')
        project = self.request.query_params.get('project_id', None)
        if project is not None:
            queryset = queryset.filter(project=project).order_by('-end_date')
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated, IsProjectParticipant]

    # perform_create and perform_update define the logged in user as assigned person directly,
    # rather than from request data:
    def perform_create(self, serializer):
        serializer.save(assigned_person=self.request.user)

    def perform_update(self, serializer):
        serializer.save(assigned_person=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned users to a given project, sprint or user&project,
        by filtering against a `project` query parameter in the URL.
        Accessible through URL: /tasks/?sprint_id='sprint_id'
        Or URL: /tasks/?project_id='project_id'
        Or URL: /tasks/?project_id='project_id'&user_id='user_id'
        """
        queryset = Task.objects.all()
        sprint = self.request.query_params.get('sprint_id', None)
        project = self.request.query_params.get('project_id', None)
        person = self.request.query_params.get('user_id', None)

        if sprint is not None:
            queryset = queryset.filter(sprints__id=sprint)
        if project is not None:
            queryset = queryset.filter(project=project)
            if person is not None:
                queryset = queryset.filter(assigned_person=person)
        return queryset
