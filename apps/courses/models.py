from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class Course(models.Model):
  name = models.CharField(max_length=255)
  teacher = models.ForeignKey(User, related_name="courses_taught")
  students = models.ManyToManyField(User, related_name="enrolled_courses")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)