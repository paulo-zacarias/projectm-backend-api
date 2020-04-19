from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Profile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ['image', 'display_name']
        extra_kwargs = {'display_name': {'read_only': True}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = UserProfileSerializer(required=False, read_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'first_name', 'last_name', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        # profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        # user.profile = Profile.objects.create(user=user, **profile)
        user.save()

        return user

    def update(self, instance, validated_data):

        # new_profile = validated_data.get('profile')
        # profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.set_password(validated_data['password'])

        instance.save()

        # profile.image = new_profile.get('image', profile.image)
        # profile.save()

        return instance
