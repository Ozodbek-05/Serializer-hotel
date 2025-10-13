from django.urls import path

from apps.hotel.views import user_view, hotels_view, rooms_view, rooms_id_view, rooms_bookings_view

app_name = 'hotel'

urlpatterns = [
    path('register/',user_view),
    path('hotels/',hotels_view),
    path('rooms/', rooms_view),
    path('rooms/<int:pk>/', rooms_id_view),
    path('rooms/<int:pk>/bookings/', rooms_bookings_view),

]