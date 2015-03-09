# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from accounts import views

urlpatterns = patterns('',
    url(r'^profile/$', login_required(views.UserUpdate.as_view()), name='profile'),
)
