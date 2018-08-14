from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^create/$', views.create, name="create"),
  url(r'^new/$', views.new, name="new"),
  url(r'^(?P<user_id>\w+)/show$', views.show, name="show")
]