from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'image', 'display_name']
        extra_kwargs = {'display_name': {'read_only': True, 'required': False}}


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # Override create method in order to save password properly
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()

        return user


class UserSerializerUpdate(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    # def validate_new_password(self, value):
    #     validate_password(value)
    #     return value