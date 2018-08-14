from django.shortcuts import render, redirect

# Create your views here.
def index(req):
  return redirect('/users/new')