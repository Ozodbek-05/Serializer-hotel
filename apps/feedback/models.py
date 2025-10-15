from django.db import models

class FeedbackModel(models.Model):
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedbacks'

    def __str__(self):
        return self.email