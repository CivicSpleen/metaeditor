from django.conf.urls import patterns, url

from editor import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),

    #url(r'^datasets/$', "editor.views.datasets"),

    url(r'^categories/$', "editor.views.categories"),
    url(r'^add_category/$', "editor.views.add_category"),

    url(r'^sources/$', "editor.views.sources"),
    url(r'^formats/$', "editor.views.formats")
)
