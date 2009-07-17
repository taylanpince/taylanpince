from django.conf import settings
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from akismet import Akismet
from prowl.prowlpy import Prowl
from xmlrpclib import ServerProxy


def moderate_comment(sender, instance, **kwargs):
    """
    Connects to the Akismet API to verify the comment's authenticity
    """
    if not instance.published:
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http://%s/" % Site.objects.get_current().domain)
    
        if akismet_api.verify_key():
            try:
                if not akismet_api.comment_check(smart_str(instance.body), data={
                    "user_ip": instance.ip_address,
                    "user_agent": "",
                    "referrer": "unknown",
                    "comment_type": "comment",
                    "comment_author": instance.author,
                    "comment_author_email": instance.email,
                    "comment_author_url": instance.url,
                }, build_data=True):
                    instance.published = True
                    
                    prowl_api = Prowl(settings.PROWL_API_KEY)
                    site = Site.objects.get_current()

                    if prowl_api.verify_key():
                        try:
                            prowl_api.post(
                                application="taylanpince.com",
                                event="New Comment",
                                description="A new comment has been published under blog post: %(title)s\r\n%(link)s" % {
                                    "title": instance.post.title,
                                    "link": "http://%(domain)s%(path)s" % {
                                        "domain": site.domain,
                                        "path": instance.post.get_absolute_url(),
                                    }
                                }
                            )
                        except Exception, message:
                            print "PROWL FAIL: %s", message
            except:
                pass


def ping_blog_indexes(sender, instance, created, **kwargs):
    """
    Ping blog indexes using XMLRPC
    """
    if created:
        site = Site.objects.get_current()
    
        for index in settings.BLOG_INDEXES:
            rpc = ServerProxy(index)
        
            try:
                rpc.weblogUpdates.extendedPing(
                    site.name, 
                    "http://%s/" % site.domain, 
                    "http://%s%s" % (site.domain, instance.get_absolute_url()), 
                    "http://%s%s" % (site.domain, reverse("feeds", kwargs={"url": "posts"}))
                )
            except:
                rpc.weblogUpdates.ping(site.name, "http://%s/" % site.domain)
