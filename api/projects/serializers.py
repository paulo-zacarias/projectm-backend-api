from .models import Project, Sprint, Task
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'admin', 'participants']

        # The admin will be automatically assigned to the currently logged in user,
        # this field will be added through the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'admin': {'required': False}}


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'weight', 'story_points', 'status', 'assigned_person', 'project', 'sprints']

        # The assigned person will be automatically assigned to the currently logged in user,
        # this field will be added through the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'assigned_person': {'required': False}}


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
    #     tasks = data['tasks']
    #     for task in tasks:
    #         if task.project.id != self.instance.project.id:
    #             raise serializers.ValidationError(f"The task {task.id} cannot be added to sprint"
    #                                               f"as they don't belong to same project {self.instance.project}.")

        return data