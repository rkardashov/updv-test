from django.contrib.auth.models import User
from rest_framework import serializers
from .helpers import get_idtype
from .helpers import IDTypes


class UserSerializer(serializers.ModelSerializer):
    ID = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['ID', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_ID(self, value):
        if get_idtype(value) == IDTypes.UNKNOWN:
            raise serializers.ValidationError("Username must be a valid email or phone number.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
