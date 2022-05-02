from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user.models import User
from django.core import exceptions


def valid_password(password):
    try:
        validate_password(password=password)
    except exceptions.ValidationError as e:
        raise e


class UserAuthorizationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[valid_password])

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)


