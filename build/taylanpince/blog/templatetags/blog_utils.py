import re

from urllib2 import HTTPError, URLError

from django import template
from django.conf import settings
from django.core.cache import cache

from twitter import Api as TwitterAPI

from blog.models import Post, Category


register = template.Library()


class RecentPostsLoader(template.Node):
    def __init__(self, limit, var_name):
        self.limit = limit
        self.var_name = var_name
    
    def __repr__(self):
        return "<RecentPostsLoader>"
    
    def render(self, context):
        try:
            posts = Post.objects.all()[:self.limit]
        except:
            posts = None
        
        context[self.var_name] = posts
        
        return ""


@register.tag
def load_recent_posts(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    
    m = re.search(r"(.*?) as (\w+)", arg)
    
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    
    limit, var_name = m.groups()
    
    return RecentPostsLoader(limit, var_name)


@register.inclusion_tag("blog/category_list.html")
def load_categories():
    return {
        "categories": Category.objects.all(),
    }


URL_RE = re.compile(r"\b%(urls)s:[%(any)s]+?(?=[%(punc)s]*(?:[^%(any)s]|$))" % {
    "urls": "(?: %s)" % "|".join("http telnet gopher file wais ftp".split()),
    "any": r"\w/#~:.?+=&%@!\-.:?\-",
    "punc": r".:?\-",
}, re.VERBOSE)

REPLY_RE = re.compile(r"@([\w]+?)\b")


@register.inclusion_tag("blog/tweets.html")
def load_recent_tweets():
    key = "recent_tweets"
    tweets = cache.get(key)
    
    if not tweets:
        try:
            api = TwitterAPI(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
            tweets = api.GetUserTimeline(settings.TWITTER_USERNAME)
        except (HTTPError, URLError, ValueError):
            tweets = []
        
        for tweet in tweets:
            tweet.text = URL_RE.sub(
                lambda m: '<a href="%(url)s">%(url)s</a>' % {"url": m.group()}, 
                tweet.text
            )
        
            tweet.text = REPLY_RE.sub(
                lambda m: '<a href="http://twitter.com/%(user)s">@%(user)s</a>' % {"user": m.group()[1:]}, 
                tweet.text
            )
    
        cache.set(key, tweets, 60 * 60)
    
    return {
        "tweets": tweets,
    }
