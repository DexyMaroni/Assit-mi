from django.db import models

class Transcription(models.Model):
    text = models.TextField()
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}... ({self.confidence})"

