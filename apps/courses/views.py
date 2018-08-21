from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course
from ..users.models import User

# Create your views here.
def index(req):
  context = {
    "courses": Course.objects.all()
  }
  return render(req, 'courses/index.html', context)

def new(req):
  context = {
    'teachers': User.objects.filter(permission_level="TEACHER")
  }
  return render(req, 'courses/new.html', context)

def create(req):
  valid, result = Course.objects.validate_and_create_course(req.POST)
  if not valid:
    for err in result:
      messages.error(req, err)
    return redirect('courses:new')

  return redirect('courses:index')