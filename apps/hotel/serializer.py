from rest_framework import serializers

from apps.hotel.models import Hotel

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64, write_only=True)
    password_confirm = serializers.CharField(max_length=64, write_only=True)
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
    phone_number = serializers.CharField(max_length=13, write_only=True000)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

