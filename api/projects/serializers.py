from .models import Project, Sprint, Task
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'admin', 'participants']

        # The admin will be automatically assigned to the currently logged in user,
        # this field will be added through the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'admin': {'required': False}}


class SprintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sprint
        fields = ['id', 'start_date', 'end_date', 'planned_story_points', 'project']

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be earlier than end date.")
        return data


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'weight', 'story_points', 'status', 'sprint', 'assigned_person']

        # The assigned person will be automatically assigned to the currently logged in user,
        # this field will be added through the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'assigned_person': {'required': False}}
