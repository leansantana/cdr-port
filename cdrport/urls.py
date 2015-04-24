from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cdrport.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^cdr/', include('cdr.urls')),
    url(r'^', include('cdr.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
