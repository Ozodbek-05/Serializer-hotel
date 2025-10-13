from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Avg
from apps.hotel.models import Booking, Hotel, Amenity, RoomType, Room
from rest_framework import serializers
from .models import RoomReview

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64, write_only=True)
    password_confirm = serializers.CharField(max_length=64, write_only=True)
    first_name = serializers.CharField(max_length=128)
    last_name = serializers.CharField(max_length=128)
    phone_number = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match!'})
        return attrs

    @staticmethod
    def validate_phone_number(value):
        if not value.startswith('+998'):
            raise serializers.ValidationError("Phone number must start with +998")
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    @staticmethod
    def validate_username(value):
        for sign in value:
            if not (sign.isalnum() or sign == '_'):
                raise serializers.ValidationError("Username must contain only letters numbers and '_'")
        return value

class HotelsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField()
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=128)
    country = serializers.CharField(max_length=128)
    star_rating = serializers.IntegerField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Hotel.objects.create(**validated_data)

    def validate(self, attrs):
        if len(attrs['description']) > 50:
            raise serializers.ValidationError("Description length should not exceed 50 characters")
        return attrs

    @staticmethod
    def validate_star_rating(value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    @staticmethod
    def validate_name(value):
        if len(value) < 5:
            raise serializers.ValidationError("The name length must not be less than 5 characters")
        return value

    @staticmethod
    def validate_phone(value):
        if not value.startswith('+998'):
            raise serializers.ValidationError("Phone number must start with +998")
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    @staticmethod
    def validate_email(value):
        if Hotel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email has already been registered")
        return value


class HotelNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    city = serializers.CharField()
    star_rating = serializers.IntegerField()


class RoomTypeNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class AmenityNestedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    icon = serializers.CharField()


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    room_number = serializers.CharField(max_length=10)
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    amenities = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Amenity.objects.all()
    )
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = serializers.IntegerField(default=0)
    capacity = serializers.IntegerField()
    floor = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Room.STATUS_CHOICES)
    description = serializers.CharField()
    final_price = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    is_available = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        amenities_ids = validated_data.pop("amenities", [])

        hotel = validated_data.pop("hotel")
        room_type = validated_data.pop("room_type")

        room = Room.objects.create(
            hotel=hotel,
            room_type=room_type,
            **validated_data
        )

        room.amenities.set(amenities_ids)
        return room


    @staticmethod
    def get_final_price(obj):
        return float(obj.price_per_night) * (1 - obj.discount_percentage / 100)

    @staticmethod
    def get_is_available(obj):
        return obj.status == "available"

    @staticmethod
    def get_reviews_count(obj):
        return obj.reviews.count()

    @staticmethod
    def get_average_rating(obj):
        avg = obj.reviews.aggregate(Avg("overall_rating"))["overall_rating__avg"]
        return round(avg or 0, 1)

    def update(self, instance, validated_data):
        amenities_ids = validated_data.pop("amenities", None)
        if amenities_ids is not None:
            instance.amenities.set(amenities_ids)

        for attrs, value in validated_data.items():
            setattr(instance,attrs,value)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["hotel"] = HotelNestedSerializer(instance.hotel).data
        data["room_type"] = RoomTypeNestedSerializer(instance.room_type).data
        data["amenities"] = AmenityNestedSerializer(instance.amenities.all(), many=True).data

        if instance.discount_percentage == 0:
            data.pop("discount_percentage", None)

        return data


    def validate(self, attrs):
        if Room.objects.filter(room_number=attrs).exists():
            raise serializers.ValidationError("This room is already booked")
        return attrs

    @staticmethod
    def validate_discount_percentage(value):
        if 0 >= value or value >= 100:
            raise serializers.ValidationError("Validate discount percentage must be between 0 and 100")
        return value

    @staticmethod
    def validate_price_per_night(value):
        if value < 0:
            raise serializers.ValidationError("Validate price per night must be greater than 0")
        return value

    @staticmethod
    def validate_floor(value):
        if value < 0:
            raise serializers.ValidationError("Validate floor must be greater than 0")
        return value

    @staticmethod
    def validate_capacity(value):
        if 1 > value or value > 10:
            raise serializers.ValidationError("Validate capacity must be between 0 and 10")
        return value


class RoomsBookingsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests_count = serializers.IntegerField()
    special_requests = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    nights_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()


    @staticmethod
    def get_user(value):
        return {
            "id": value.user.id,
            "username":value.user.username
        }

    @staticmethod
    def get_room(value):
        return {
            "id":value.room.id,
            "room_number": value.room.room_number,
            "hotel_name": value.room.hotel.name
        }

    @staticmethod
    def get_nights_count(value):
        return (value.check_out - value.check_in).days
    
    @staticmethod
    def check_in_date(value):
        if value < date.today():
            raise serializers.ValidationError("Check-in date must not be before today")
        return value
    
    def validate_check_out(self, value):
        check_in = self.initial_data.get("check_in")
        if check_in and str(value) < check_in:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        return value
    
    def validate_guesta_count(self,value):
        room = serializers.context.get("room")
        if room and value > room.capacity:
            raise serializers.ValidationError("Guests count exceeds room capacity")
        return value
    
    def validate(self, attrs):
        room = self.context.get("room")
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        
        if room and check_in and check_out:
            overlap = Booking.objects.filter(
                room=room,
                status__in=["pending", "confirmed"],
                check_in__lt=check_out,
                check_out__gt=check_in
            ) 
            
            if overlap.exists(): 
                raise serializers.ValidationError("The room is not available for the selected dates")
            
        return attrs

        
    def create(self, validated_data):
        room = self.context.get("room")
        user = self.context.get("user")

        nights = (validated_data["check_out"] - validated_data["check_in"]).days
        discount = Decimal(room.discount_percentage) / Decimal("100")
        total_price = room.price_per_night * nights * (Decimal("1") - discount)

        booking = Booking.objects.create(
            user=user,
            room=room,
            total_price=total_price,
            **validated_data
        )
        return booking
    


class HotelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    star_rating = serializers.IntegerField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    rooms_count = serializers.SerializerMethodField()

    def get_rooms_count(self, obj):
        return obj.rooms.count()


class RoomTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()


class AmenitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.CharField()


class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cleanliness_rating = serializers.IntegerField()
    comfort_rating = serializers.IntegerField()
    service_rating = serializers.IntegerField()
    overall_rating = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField()
    average_rating = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username
        }

    def get_average_rating(self, obj):
        ratings = [
            obj.cleanliness_rating,
            obj.comfort_rating,
            obj.service_rating,
            obj.overall_rating
        ]
        return round(sum(ratings) / 4, 2)


class RoomDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hotel = HotelSerializer()
    room_number = serializers.CharField()
    room_type = RoomTypeSerializer()
    amenities = AmenitySerializer(many=True)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = serializers.IntegerField()
    capacity = serializers.IntegerField()
    floor = serializers.IntegerField()
    status = serializers.CharField()
    description = serializers.CharField()
    reviews = ReviewSerializer(many=True)
    reviews_count = serializers.SerializerMethodField()
    average_cleanliness = serializers.SerializerMethodField()
    average_comfort = serializers.SerializerMethodField()
    average_service = serializers.SerializerMethodField()
    overall_average_rating = serializers.SerializerMethodField()

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_cleanliness(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.cleanliness_rating for r in reviews) / len(reviews), 2)

    def get_average_comfort(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.comfort_rating for r in reviews) / len(reviews), 2)

    def get_average_service(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.service_rating for r in reviews) / len(reviews), 2)

    def get_overall_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.overall_rating for r in reviews) / len(reviews), 2)


class ReviewCreateSerializer(serializers.Serializer):
    cleanliness_rating = serializers.IntegerField()
    comfort_rating = serializers.IntegerField()
    service_rating = serializers.IntegerField()
    overall_rating = serializers.IntegerField()
    comment = serializers.CharField()


    def validate(self, attrs):
        user = self.context.get("user")
        room = self.context.get("room")

        if not user or not room:
            raise serializers.ValidationError("User or room not found in context")

        if RoomReview.objects.filter(user=user, room=room).exists():
            raise serializers.ValidationError("You have already left a review for this room")

        if len(attrs.get("comment", "")) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long")

        return attrs

    def create(self, validated_data):
        user = self.context.get("user")
        room = self.context.get("room")
        review = RoomReview.objects.create(user=user, room=room, **validated_data)
        return review
    

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if "comment" in data and isinstance(data["comment"], str):
            data["comment"] = data["comment"].strip()
        return data

    def validate_cleanliness_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Cleanliness rating must be between 1 and 5")
        return value

    def validate_comfort_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Comfort rating must be between 1 and 5")
        return value

    def validate_service_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Service rating must be between 1 and 5")
        return value

    def validate_overall_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Overall rating must be between 1 and 5")
        return value

    