# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from editor import views

urlpatterns = [
    url(r'^dataset/source/(?P<source_pk>[0-9]+)/create$',
        login_required(views.DatasetCreate.as_view()),
        name='dataset-create'),
    url(r'^dataset/(?P<pk>[0-9]+)/$',
        views.DatasetUpdate.as_view(),
        name='dataset-update'),

    url(r'^category$',
        views.CategoryList.as_view(),
        name='category-list'),
    url(r'^category/create$',
        login_required(views.CategoryCreate.as_view()),
        name='category-create'),
    url(r'^category/(?P<pk>[0-9]+)$',
        views.CategoryUpdate.as_view(),
        name='category-update'),

    url(r'^source$',
        views.SourceList.as_view(),
        name='source-list'),
    url(r'^source/create$',
        login_required(views.SourceCreate.as_view()),
        name='source-create'),
    url(r'^source/(?P<pk>[0-9]+)$',
        views.SourceUpdate.as_view(),
        name='source-update'),

    url(r'^format$',
        views.FormatList.as_view(),
        name='format-list'),
    url(r'^format/create$',
        login_required(views.FormatCreate.as_view()),
        name='format-create'),
    url(r'^format/(?P<pk>[0-9]+)$',
        views.FormatUpdate.as_view(),
        name='format-update'),
    url(r'^scrape$',
        views.scrape,
        name='scrape'),
    url(r'^validate-url$',
        views.validate_url,
        name='validate-url'),
    url(r'^coverage-list$',
        views.coverage_list,
        name='coverage-list'),
]
