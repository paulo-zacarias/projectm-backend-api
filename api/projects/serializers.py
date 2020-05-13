from .models import Project, Sprint, Task
from rest_framework import serializers
from users.serializers import UserSerializer


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
        Workaround to solve issue with date validation, that would prevent adding new tasks
        POST and PUT will check for start and end dates, those should be used to create and edit sprint, respectively
        PATCH should be used when only adding new tasks (skips date validation)
        """
        # First check if the start and end date are present, for POST and PUT method:
        if data.get('start_date') and data.get('end_date') is not None:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start date must be earlier than end date.")

            sprints = Sprint.objects.all().filter(project=self.initial_data['project'])
            # If instance exists, means it is a PUT request and the sprint to be updated should be exclude from de query
            if self.instance is not None:
                sprint_id = self.instance.id
                latest_sprint = sprints.exclude(id=sprint_id).latest('end_date')
            # Other, if instance doesn't exit, means it is a POST request so we query all sprints
            else:
                latest_sprint = sprints.latest('end_date')
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
    assigned_person = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'weight', 'story_points', 'status', 'project', 'assigned_person']

    def create(self, validated_data):
        user = validated_data.pop('assigned_person')
        instance = Task.objects.create(**validated_data)
        instance.assigned_person = user
        instance.save
        return instance

    def update(self, instance, validated_data):
        user = validated_data.pop('assigned_person')

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.story_points = validated_data.get('story_points', instance.story_points)
        instance.status = validated_data.get('status', instance.status)
        instance.project = validated_data.get('project', instance.project)
        instance.assigned_person = user
        instance.save()

        return instance
