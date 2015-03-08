from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
    url(r'^profile/$', views.profile, name='profile'),
)
