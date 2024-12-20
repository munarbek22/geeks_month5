from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=155)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists')

class ConfirmationCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)

    def validate_code(self, code):
        if not ConfirmationCode.objects.filter(code=code).exists():
            raise serializers.ValidationError("Invalid confirmation code.")
        return code