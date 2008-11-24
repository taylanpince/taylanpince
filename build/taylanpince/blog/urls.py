from django.conf.urls.defaults import *


urlpatterns = patterns("blog.views",
    # Landing
    url(r"^$", "landing", name="blog_landing"),
    
    # Post Detail
    url(r"^posts/(?P<slug>[-\w]+)/$", "post_detail", name="blog_post_detail"),
    
    # Category Detail
    url(r"^categories/(?P<slug>[-\w]+)/$", "category_detail", name="blog_category_detail"),
)
