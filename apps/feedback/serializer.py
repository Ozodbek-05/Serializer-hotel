from rest_framework import serializers

from apps.feedback.models import FeedbackModel


class FeedbackSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField()

    def create(self, validated_data):
        feedback = FeedbackModel.objects.create(
            email=validated_data['email'],
            message=validated_data['message'],
        )
        return feedback
    @staticmethod
    def validate_email(value):
        if FeedbackModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email has already been registered")
        return value

    @staticmethod
    def validate_message(value):
        if value < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long")
        return value