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

def login(req):
  if req.method != "POST":
    return redirect('users:new')

  valid, result = User.objects.login_user(req.POST)
  if not valid:
    for err in result:
      messages.error(req, err)
    return redirect('users:new')

  req.session['user_id'] = result
  return redirect('users:index')

def logout(req):
  req.session.clear()
  return redirect('dashboard:index')

def show(req, user_id):
  if 'user_id' not in req.session:
    return redirect('users:new')

  try:
    user = User.objects.get(id=user_id)
  except:
    return redirect('users:index')

  context = {
    'name': user.name,
    'email': user.email,
    'permission_level': user.permission_level,
    'courses_taught': user.courses_taught.all(),
    'enrolled_courses': user.enrolled_courses.all()
  }
  return render(req, 'users/show.html', context)

def edit(req, user_id):
  if 'user_id' not in req.session:
    return redirect('users:new')

  try:
    user = User.objects.get(id=user_id)
  except:
    return redirect('users:index')

  context = {
    'user': user
  }
  return render(req, 'users/edit.html', context)

def update(req, user_id):
  if req.method == "POST":
    valid, result = User.objects.validate_and_update_user(user_id, req.POST)
    if not valid:
      for err in result:
        messages.error(req, err)
      return redirect('users:edit', user_id=user_id)

  return redirect('users:index')

def delete(req, user_id):
  if req.method == 'POST':
    User.objects.delete_user_by_id(user_id)
  return redirect('users:index')