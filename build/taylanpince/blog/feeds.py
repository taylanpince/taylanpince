from django.core.urlresolvers import reverse
from django.contrib.syndication.feeds import Feed

from blog.models import Category, Post


class RssLatestPosts(Feed):
    title_template = "feeds/post_title.html"
    description_template = "feeds/post_description.html"
    
    title = "Taylan Pince - Blog Posts"
    
    def link(self):
        return reverse("blog_landing")
    
    description = "Latest blog posts from taylanpince.com"
    
    def items(self):
        return Post.objects.all()[:15]


class RssLatestPostsByCategory(Feed):
    title_template = "feeds/post_title.html"
    description_template = "feeds/post_description.html"
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        
        return Category.objects.get(slug__exact=bits[0])
    
    def title(self, obj):
        return "Taylan Pince - Blogs Posts Listed Under %s" % obj.title
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        
        return reverse("blog_category_detail", kwargs={
            "slug": obj.slug,
        })
    
    def description(self, obj):
        return "Latest blog posts listed under %(category)s from taylanpince.com" % {
            "category": obj.title,
        }
    
    def items(self, obj):
        return obj.post_set.all()[:15]
