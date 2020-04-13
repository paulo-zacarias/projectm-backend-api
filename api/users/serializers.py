from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ['image', 'display_name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'profile']