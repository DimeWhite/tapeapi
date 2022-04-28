from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from user.models import User
from django.core import exceptions


def valid_password(password):
    try:
        validate_password(password=password)
    except exceptions.ValidationError as e:
        raise e


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[valid_password])

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        try:
            if self.context['request'].method in ['POST']:
                pass
            elif self.context['request'].method in ['GET']:
                self.fields.pop('password')

        except KeyError:
            pass

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)


