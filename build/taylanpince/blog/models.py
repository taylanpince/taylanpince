from django.db import models
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from core.utils.parsers import parse_markdown
from core.utils.fields import AutoSlugField, CreateDateTimeField, ChangeDateTimeField

from blog.managers import PostManager


class Category(models.Model):
    """
    A blog category that posts will be listed under
    """
    title = models.CharField(_("Title"), max_length=100)
    slug = AutoSlugField(_("Slug"), populate_from="title")
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_category_detail", (), {
            "slug": self.slug,
        })
    
    def __unicode__(self):
        return self.title


class PostType(models.Model):
    """
    A blog post type
    """
    title = models.CharField(_("Title"), max_length=100)
    slug = AutoSlugField(_("Slug"), populate_from="title")
    icon = models.ImageField(_("Icon"), upload_to="blog/icons", blank=True, null=True)
    
    class Meta:
        verbose_name = _("Post Type")
        verbose_name_plural = _("Post Types")
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_posttype_detail", (), {
            "slug": self.slug,
        })
    
    def __unicode__(self):
        return self.title


class Post(models.Model):
    """
    A blog post
    """
    # Content
    title = models.CharField(_("Title"), max_length=255)
    teaser = models.TextField(_("Teaser"), blank=True)
    body = models.TextField(_("Body"), blank=True)
    link = models.URLField(_("Link"), blank=True, null=True, verify_exists=True)
    tags = TagField()
    
    # Relations
    categories = models.ManyToManyField("blog.Category", verbose_name=_("Categories"))
    type = models.ForeignKey("blog.PostType", verbose_name=_("Type"))
    
    # Time Stamps
    creation_date = CreateDateTimeField(_("Creation Date"), editable=True)
    change_date = ChangeDateTimeField(_("Change Date"))
    
    # Publishing
    published = models.BooleanField(_("Published"), default=True)
    slug = AutoSlugField(_("Slug"), populate_from="title")
    
    # Managers
    admin_objects = models.Manager()
    objects = PostManager()
    
    @property
    def body_html(self):
        """
        Parses the body field using markdown and pygments, caches the results
        """
        key = "blog_posts_body_%s" % self.pk
        html = cache.get(key)
        
        if not html:
            html = parse_markdown(self.body)
            cache.set(key, html, 60 * 60 * 24 * 30)
        
        return mark_safe(html)
    
    @property
    def teaser_html(self):
        """
        Parses the teaser field using markdown and pygments, caches the results
        """
        key = "blog_posts_teaser_%s" % self.pk
        html = cache.get(key)

        if not html:
            html = parse_markdown(self.teaser)
            cache.set(key, html, 60 * 60 * 24 * 30)

        return mark_safe(html)
    
    def save(self):
        if self.pk:
            cache.delete("blog_posts_body_%s" % self.pk)
            cache.delete("blog_posts_teaser_%s" % self.pk)
        
        super(Post, self).save()
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {
            "slug": self.slug,
        })
    
    def __unicode__(self):
        return self.title
