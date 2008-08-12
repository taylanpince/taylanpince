from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",
    # Admin
    (r"^admin/(.*)", admin.site.root),
)
