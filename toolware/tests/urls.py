from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.sites.models import Site

Site.objects.get_or_create(name='unittest', domain='unitest.org')



admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
)
