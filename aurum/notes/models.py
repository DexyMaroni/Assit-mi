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



class LectureNote(models.Model):
    COURSE_CHOICES = [
        ('Science', 'Science'),
        ('Arts', 'Arts'),
        ('History', 'History'),
        ('Politics', 'Politics'),
        ('Mathematics', 'Mathematics'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lecture_notes")
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    lecture_date = models.DateField(auto_now_add=True)
    instructor_name = models.CharField(max_length=200, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    subject = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class LectureAttachment(models.Model):
    lecture_note = models.ForeignKey(LectureNote, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="lecture_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.lecture_note.title}"