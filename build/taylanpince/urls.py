from django.conf.urls.defaults import *


urlpatterns = patterns("",
    # Admin
    (r"^admin/", include("django.contrib.admin.urls")),
)
