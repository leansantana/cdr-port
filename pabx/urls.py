# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cdrport.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^pabx/$', views.pabx, name='pabx'),
    url(r'^ramal/$', views.editar_ramal, name='editar_ramal'),
    url(r'^ramal/(?P<name>\d+)/$', views.editar_ramal, name='editar_ramal'),

)
