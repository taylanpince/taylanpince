from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils.fields import AutoSlugField, CreateDateTimeField

from portfolio.managers import PieceManager


class Category(models.Model):
    """
    A portfolio category
    """
    title = models.CharField(_("Title"), max_length=255)
    slug = AutoSlugField(_("Slug"), populate_from="title")

    @property
    def pieces(self):
        return Piece.objects.filter(categories=self)

    def get_absolute_url(self):
        return "%(url)s?category=%(slug)s" % {
            "url": reverse("home"),
            "slug": self.slug,
        }

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.title


class Photo(models.Model):
    """
    An image file tied to a portfolio piece
    """
    title = models.CharField(_("Title"), max_length=255)
    image = models.ImageField(_("Image"), upload_to="files/portfolio")
    piece = models.ForeignKey("portfolio.Piece", verbose_name=_("Piece"))
    thumbnail = models.BooleanField(_("Thumbnail"), default=False)

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")

    def __unicode__(self):
        return self.title


class Piece(models.Model):
    """
    A portfolio piece
    """
    # Content
    title = models.CharField(_("Title"), max_length=255)
    teaser = models.TextField(_("Teaser"), blank=True)
    body = models.TextField(_("Body"), blank=True)
    client = models.CharField(_("Client"), blank=True, max_length=255)
    responsibilities = models.TextField(_("Responsibilities"), blank=True)
    link = models.URLField(_("Link"), blank=True, null=True, verify_exists=True)

    # Relations
    categories = models.ManyToManyField("portfolio.Category", verbose_name=_("Categories"))

    # Publishing
    slug = AutoSlugField(_("Slug"), populate_from="title")
    published = models.BooleanField(_("Published"), default=True)
    creation_date = CreateDateTimeField(_("Creation Date"), editable=True)
    
    # Managers
    admin_objects = models.Manager()
    objects = PieceManager()

    @property
    def photos(self):
        return Photo.objects.filter(piece=self, thumbnail=False).order_by("pk")

    @property
    def thumbnail(self):
        try:
            return Photo.objects.filter(piece=self, thumbnail=True)[0]
        except IndexError:
            return None

    class Meta:
        verbose_name = _("Piece")
        verbose_name_plural = _("Pieces")

    @models.permalink
    def get_absolute_url(self):
        return ("portfolio_detail", (), {
            "slug": self.slug,
        })

    def __unicode__(self):
        return self.title
