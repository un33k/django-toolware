from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.sites.models import Site

admin.autodiscover()
Site.objects.get_or_create(name='unittest', domain='unitest.org')

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
)
