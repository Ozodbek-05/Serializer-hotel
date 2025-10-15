from rest_framework import generics
from apps.feedback.models import FeedbackModel
from apps.feedback.serializer import FeedbackSerializer


class FeedbackView(generics.RetrieveUpdateAPIView):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer