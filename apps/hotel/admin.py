from django.contrib import admin
from .models import CustomUser, Hotel, RoomType, Amenity, Room, Booking, RoomReview
from django.contrib.auth.admin import UserAdmin

# 🔹 CustomUser uchun admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "phone_number", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)

# 🔹 Hotel
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "star_rating", "phone", "email")
    search_fields = ("name", "city", "country", "email")
    list_filter = ("city", "country", "star_rating")

# 🔹 RoomType
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

# 🔹 Amenity
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)

# 🔹 Room
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "hotel", "room_type", "capacity", "floor", "status", "price_per_night", "discount_percentage")
    list_filter = ("status", "hotel", "room_type", "floor")
    search_fields = ("room_number", "hotel__name", "room_type__name")
    filter_horizontal = ("amenities",)

# 🔹 Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "check_in", "check_out", "guests_count", "total_price", "status")
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("room__room_number", "user__username")

# 🔹 RoomReview
@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "overall_rating", "cleanliness_rating", "comfort_rating", "service_rating", "created_at")
    list_filter = ("overall_rating", "created_at")
    search_fields = ("room__room_number", "user__username", "comment")
