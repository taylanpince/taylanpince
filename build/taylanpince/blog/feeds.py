from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

from tagging.models import Tag, TaggedItem

from blog.models import Category, Post


class RssLatestPosts(Feed):
    title_template = "feeds/post_title.html"
    description_template = "feeds/post_description.html"
    
    feed_type = Atom1Feed
    
    title = "Taylan Pince - Blog Posts"
    subtitle = "Latest blog posts from taylanpince.com"
    author_name = "Taylan Pince"
    copyright = "Copyright (c) 2008, Taylan Pince"
    
    def link(self):
        return "http://%s%s" % (Site.objects.get_current().domain, reverse("blog_landing"))
    
    def items(self):
        return Post.objects.all()[:15]
    
    def item_pubdate(self, item):
        return item.creation_date
    
    def item_categories(self, item):
        return [t.name for t in Tag.objects.get_for_object(item)]


class RssLatestPostsByCategory(RssLatestPosts):
    def title(self, obj):
        return "Taylan Pince - Blogs Posts Listed Under %s" % obj.title
    
    def description(self, obj):
        return "Latest blog posts listed under %(category)s from taylanpince.com" % {
            "category": obj.title,
        }
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        
        return reverse("blog_category_detail", kwargs={
            "slug": obj.slug,
        })
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        
        return Category.objects.get(slug__exact=bits[0])
    
    def items(self, obj):
        return Post.objects.filter(categories=obj)[:15]


class RssLatestPostsByTag(RssLatestPosts):
    def title(self, obj):
        return "Taylan Pince - Blogs Posts Tagged As %s" % obj.name
    
    def description(self, obj):
        return "Latest blog posts tagged as %(category)s from taylanpince.com" % {
            "category": obj.name,
        }
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        
        return reverse("blog_tag_detail", kwargs={
            "tag": obj.name,
        })
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        
        return Tag.objects.get(name__exact=bits[0])
    
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Post.objects, obj)[:15]
