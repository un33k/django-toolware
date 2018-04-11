from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.sites.models import Site

admin.autodiscover()
Site.objects.get_or_create(name='unittest', domain='unitest.org')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
