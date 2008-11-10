from django.contrib import admin
from django.conf.urls.defaults import *


admin.autodiscover()


urlpatterns = patterns('',
    # Admin
    (r'^admin/(.*)', admin.site.root),
    
    # Application Form
    url(r'^$', 'applications.views.application_form', name='application_form'),
    
    # Application Complete
    url(r'^complete/$', 'django.views.generic.simple.direct_to_template', {
        "template": "applications/complete.html",
    }, name='application_complete'),
)
