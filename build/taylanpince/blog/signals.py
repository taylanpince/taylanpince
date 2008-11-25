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
        if akismet_api.comment_check(smart_str(instance.body), data={
            "comment_type": "comment",
            "referrer": "",
            "user_ip": instance.ip_address,
            "user_agent": "",
        }, build_data=True):
            instance.published = False
        else:
            instance.published = True
