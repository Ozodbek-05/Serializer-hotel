from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # 🔹 bu qo‘shiladi

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.username


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    star_rating = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenity, related_name='rooms')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField(default=0)  # 0-100
    capacity = models.IntegerField()
    floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')  # 🔹 o‘zgartirildi
    check_in = models.DateField()
    check_out = models.DateField()
    guests_count = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RoomReview(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 🔹 o‘zgartirildi
    cleanliness_rating = models.IntegerField()  # 1-5
    comfort_rating = models.IntegerField()  # 1-5
    service_rating = models.IntegerField()  # 1-5
    overall_rating = models.IntegerField()  # 1-5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
