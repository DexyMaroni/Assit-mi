from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# Sticky Note Model
class StickyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Lecture Note Model
class LectureNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    date = models.DateField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} - {self.instructor}"

# Event Model (for calendar)
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# Study Group Model
class StudyGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_private = models.BooleanField(default=True)
    members = models.ManyToManyField(User, related_name='study_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name