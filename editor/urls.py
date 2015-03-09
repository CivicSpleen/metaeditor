# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from editor import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^dataset/$',
        views.DatasetList.as_view(),
        name='dataset-list'),
    url(r'^dataset/source/(?P<source_pk>[0-9]+)/create/$',
        login_required(views.DatasetCreate.as_view()),
        name='dataset-create'),
    url(r'^dataset/(?P<pk>[0-9]+)/$',
        login_required(views.DatasetUpdate.as_view()),
        name='dataset-update'),

    url(r'^category/$',
        views.CategoryList.as_view(),
        name='category-list'),
    url(r'^category/create/$',
        views.CategoryCreate.as_view(),
        name='category-create'),
    url(r'^category/(?P<pk>[0-9]+)/$',
        views.CategoryUpdate.as_view(),
        name='category-update'),

    url(r'^source/$',
        views.SourceList.as_view(),
        name='source-list'),
    url(r'^source/create/$',
        views.SourceCreate.as_view(),
        name='source-create'),
    url(r'^source/(?P<pk>[0-9]+)/$',
        views.SourceUpdate.as_view(),
        name='source-update'),

    url(r'^format/$',
        views.FormatList.as_view(),
        name='format-list'),
    url(r'^format/create/$',
        views.FormatCreate.as_view(),
        name='format-create'),
    url(r'^format/(?P<pk>[0-9]+)/$',
        views.FormatUpdate.as_view(),
        name='format-update'),
)
