from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ['image', 'display_name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'profile']

        def update(self, instance, validated_data):

            new_profile = validated_data.get('profile')
            profile = instance.profile

            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.save()

            profile.image = new_profile.get('image', profile.image)
            profile.save()

            return instance

            # profile = validated_data.pop('profile')
            # user = User.objects.update(**validated_data)
            # Profile.objects.update(user=user, **profile)
            # return user
