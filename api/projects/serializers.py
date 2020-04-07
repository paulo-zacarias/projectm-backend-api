from .models import Project
from rest_framework import serializers


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    # entries = EntriesSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['url', 'name', 'description', 'admin', 'participants']