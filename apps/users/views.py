from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(req):
  if 'user_id' not in req.session:
    return redirect('users:new')

  context = {
    'users': User.objects.all()
  }
  return render(req, 'users/index.html', context)

def new(req):
  return render(req, 'users/new.html')

def create(req):
  if req.method != 'POST':
    return redirect('users:new')

  valid, result = User.objects.validate_and_create_user(req.POST)
  if not valid:
    for err in result:
      messages.error(req, err)
    return redirect('users:new')

  req.session['user_id'] = result
  return redirect('users:index')

def show(req, user_id):
  # print user_id, "THIS IS THE USER ID"
  user_id = int(user_id)
  user = req.session['users'][user_id]
  # print user

  context = {
    'name': user['name'],
    'email': user['email'],
    'permission_level': user['permission_level']
  }
  return render(req, 'users/show.html', context)