from rest_framework import serializers
from django.utils.text import slugify

from apps.blogs.models import BlogProfile, Category
from apps.hotel.models import CustomUser


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    bio = serializers.CharField(max_length=255,required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(max_length=128, write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        bio = validated_data.pop('bio', None)
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if bio:
            BlogProfile.objects.create(user=user, bio=bio)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep['bio'] = instance.blogprofile.bio
        except BlogProfile.DoesNotExist:
            rep['bio'] = None
        return rep


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        bio = attrs.get('bio')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords does not match!")
        if bio is not None and len(bio) <= 20:
            raise serializers.ValidationError("Bio should contain at least 20 characters!")
        return attrs


    @staticmethod
    def validate_username(value):
        if not all(ch.isalnum() or ch == '_' for ch in value):
            raise serializers.ValidationError(
                "Username can contain only letters, numbers, and underscores (_)."
            )
        return value


    @staticmethod
    def validate_email(value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value


    @staticmethod
    def validate_password(value):
        has_upper = False
        has_digit = False

        for char in value:
            if char.isupper():
                has_upper = True
            if char.isdigit():
                has_digit = True

        if not has_upper:
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not has_digit:
            raise serializers.ValidationError("Password must contain at least one digit.")

        return value

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return Category.objects.create(**validated_data)

    def validate(self, attrs):
        if len(attrs.get('description')) < 30:
            raise serializers.ValidationError("Description length should not be less than 30 characters")
        return attrs

    def to_internal_value(self, data):
        data = data.copy()
        if 'name' in data and isinstance(data['name'], str):
            data['name'] = data['name'].strip()
        return super().to_internal_value(data)

    @staticmethod
    def validate_name(value):
        if len(value) < 3:
            raise serializers.ValidationError("The name should be more than 3")
        elif not value[0].isupper():
            raise serializers.ValidationError("Name must start with an uppercase letter.")
        return value