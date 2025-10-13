from django.urls import path

from apps.blogs.views import user_register, category_view

app_name = 'blogs'

urlpatterns = [
    path('register/', user_register),
    path('category/', category_view),
]