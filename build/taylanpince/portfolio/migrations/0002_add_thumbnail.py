from django.db import models
from django.utils.translation import ugettext_lazy as _

from south.db import db

from portfolio.models import *


class Migration:
    def forwards(self):
        # Adding field 'Photo.thumbnail'
        db.add_column('portfolio_photo', 'thumbnail', models.BooleanField(_("Thumbnail"), default=False))
    
    def backwards(self):
        # Deleting field 'Photo.thumbnail'
        db.delete_column('portfolio_photo', 'thumbnail')
