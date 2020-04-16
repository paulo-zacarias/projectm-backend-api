from .models import Project, Sprint, Task
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ['url', 'name', 'description', 'admin', 'participants']

        # The admin will be automatically assigned to the currently logged in user,
        # this field will be added in the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'admin': {'required': False}}


class SprintSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sprint
        fields = ['url', 'start_date', 'end_date', 'planned_story_points', 'project']


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ['url', 'name', 'description', 'story_points', 'status', 'sprint', 'assigned_person']