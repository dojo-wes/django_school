from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
  def validate_and_create_user(self, form_data):
    errors = []

    if len(form_data['name']) < 2:
      errors.append('Name must be at least 2 characters')
    if not EMAIL_REGEX.match(form_data['email']):
      errors.append('Must use a valid email address')
    if len(form_data['password']) < 8:
      errors.append('Name must be at least 2 characters')
    if form_data['password'] != form_data['confirm']:
      errors.append('Passwords must match')

    if errors:
      return (False, errors)

    # check for existence of a user
    try:
      existing_user = self.get(email=form_data['email'])
      errors.append('Email already exists.')
      return (False, errors)
    except:
      pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
      user = self.create(name=form_data['name'], email=form_data['email'], pw_hash=pw_hash, permission_level="STUDENT")

    return (True, user.id)

  def login_user(self, form_data):
    errors = []

    try:
      user = self.get(email=form_data['email'])
      # check to see if passwords match
      if not bcrypt.checkpw(form_data['password'].encode(), user.pw_hash.encode()):
        errors.append('Username or password is invalid')
        return (False, errors)
      
      return (True, user.id)
    except:
      errors.append('Username or password is invalid')
      return (False, errors)

  def validate_and_update_user(self, user_id, form_data):
    errors = []

    if len(form_data['name']) < 2:
      errors.append('Name must be at least 2 characters')
    if not EMAIL_REGEX.match(form_data['email']):
      errors.append('Must use a valid email address')

    if errors:
      return (False, errors)

    try:
      user = self.get(id=user_id)
      user.name = form_data['name']
      user.email = form_data['email']
      user.save()
      return (True, user)
    except:
      errors.append("User doesn't exist")
      return (False, errors)

  def delete_user_by_id(self, user_id):
    try:
      user = self.get(id=user_id)
      user.delete()
      return True
    except:
      return False


class User(models.Model):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  pw_hash = models.CharField(max_length=500)
  permission_level = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __str__(self):
    return self.email