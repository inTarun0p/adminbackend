from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'country', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures password is write-only and won't be included in responses
        }

    def create(self, validated_data):
        # Create and return a new User instance, given the validated data
        return User.objects.create(**validated_data)
