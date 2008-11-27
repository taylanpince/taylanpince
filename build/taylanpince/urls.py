from django.contrib import admin
from django.conf.urls.defaults import *

from blog.feeds import RssLatestPosts, RssLatestPostsByCategory, RssLatestPostsByTag


admin.autodiscover()


urlpatterns = patterns("",
    # Admin
    (r"^admin/(.*)", admin.site.root),
    
    # Home
    url(r"^$", "django.views.generic.simple.direct_to_template", {
        "template": "home.html",
    }, name="home"),
    
    # Blog
    (r"^blog/", include("blog.urls")),
    
    # Work
    url(r"^work/$", "django.views.generic.simple.direct_to_template", {
        "template": "work.html",
    }, name="work"),
    
    # About
    url(r"^about/$", "django.views.generic.simple.direct_to_template", {
        "template": "about.html",
    }, name="about"),
    
    # Feeds
    url(r"^feeds/(?P<url>.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": {
            "posts": RssLatestPosts,
            "posts-by-category": RssLatestPostsByCategory,
            "posts-by-tag": RssLatestPostsByTag,
        }
    }, name="feeds"),
)
