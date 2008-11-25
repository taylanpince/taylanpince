from django.conf import settings
from django.utils.encoding import smart_str
from django.contrib.sites.models import Site

from akismet import Akismet


def moderate_comment(sender, instance, **kwargs):
    """
    Connects to the Akismet API to verify the comment's authenticity
    """
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
        except:
            pass