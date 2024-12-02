from django.db import models
from django.conf import settings

class StickyNote(models.Model):
    REMINDER = 'Reminder'
    GOAL = 'Goal'
    THOUGHT = 'Thought'
    LOG = 'Log'
    MISC = 'Miscellaneous'

    CATEGORY_CHOICES = [
        (REMINDER, 'Reminder'),
        (GOAL, 'Goal'),
        (THOUGHT, 'Thought'),
        (LOG, 'Log'),
        (MISC, 'Miscellaneous'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=REMINDER)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sticky_notes'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation time
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated on save

    def __str__(self):
        return f"{self.title} ({self.category})"

class Attachment(models.Model):
    sticky_note = models.ForeignKey(
        StickyNote, related_name='attachments', on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="sticky_notes/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.sticky_note.title} - {self.file.name}"
