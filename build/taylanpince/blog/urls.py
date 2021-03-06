from django.conf.urls.defaults import *


urlpatterns = patterns("blog.views",
    # Landing
    url(r"^$", "landing", name="blog_landing"),
    
    # Post Detail
    url(r"^posts/(?P<slug>[-\w]+)/$", "post_detail", name="blog_post_detail"),
    
    # Submit Comment
    url(r"^posts/(?P<slug>[-\w]+)/comment/$", "submit_comment", name="blog_submit_comment"),
    
    # Category Detail
    url(r"^categories/(?P<slug>[-\w]+)/$", "category_detail", name="blog_category_detail"),
    
    # Comment Detail
    url(r"^comments/(?P<id>[0-9]+)/$", "comment_detail", name="blog_comment_detail"),
    
    # Tag Detail
    url(r"^tags/(?P<tag>[a-zA-Z0-9\.]+)/$", "tag_detail", name="blog_tag_detail"),
    
    # Post Type Styles
    url(r"^post_types\.css$", "post_type_styles", name="blog_post_type_styles"),
)
