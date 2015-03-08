from django.conf.urls import patterns, url

from editor import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),

    #url(r'^datasets/$', "editor.views.datasets"),

    url(r'^categories/$', 'editor.views.categories', name='category-list'),
    url(r'^add_category/$', 'editor.views.add_category', name='add-category'),

    url(r'^sources/$', 'editor.views.sources', name='source-list'),
    url(r'^formats/$', 'editor.views.formats', name='format-list')
)
