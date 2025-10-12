from django.urls import path

from apps.hotel.views import user_view

app_name = 'hotel'

urlpatterns = [
    path('register/',user_view)
]