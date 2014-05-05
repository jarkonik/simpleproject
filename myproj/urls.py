from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


import myapp.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', myapp.views.HomeView.as_view(), name='home'),
)
