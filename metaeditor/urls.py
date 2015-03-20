# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from editor import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^editor/', include('editor.urls', namespace='editor')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
