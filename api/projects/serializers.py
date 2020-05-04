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
        fields = ['id', 'start_date', 'end_date', 'planned_story_points', 'project', 'tasks']

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        # First check if the start and end date are present, meaning it is either POST or PUT request:
        if data.get('start_date') and data.get('end_date') is not None:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date must be earlier than end date.")

            latest_sprint = Sprint.objects.all().filter(project=self.initial_data['project']).latest('end_date')
            if data['start_date'] < latest_sprint.end_date:
                raise serializers.ValidationError(f"Overlapping sprints are not allowed!"
                                                  f"Latest sprint in this project ends on {latest_sprint.end_date}")
        # Otherwise it is PATCH request, meaning it's just adding new tasks to the sprint:
        else:
            tasks = data['tasks']
            for task in tasks:
                if task.project.id != self.instance.project.id:
                    raise serializers.ValidationError(f"The task {task.title} cannot be added to sprint"
                                                      f"as they don't belong to same project {self.instance.project}.")

        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'weight', 'story_points', 'status', 'assigned_person', 'project']

        # The assigned person will be automatically assigned to the currently logged in user,
        # this field will be added through the Project's view (create method) and is not required in the serializer
        extra_kwargs = {'assigned_person': {'required': False}}