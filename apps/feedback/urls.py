from django.urls import path

from apps.feedback.views import FeedbackView

app_name = 'feedback'

urlpatterns = [
    path('email/',FeedbackView.as_view())
]