from django.db import models
from django.utils.translation import ugettext_lazy as _

from south.db import db

from blog.models import *


class Migration:
    
    def forwards(self):
        
        # Adding field 'Post.allow_comments'
        db.add_column('blog_post', 'allow_comments', models.BooleanField(_("Allow Comments"), default=True))
        
    
    def backwards(self):
        
        # Deleting field 'Post.allow_comments'
        db.delete_column('blog_post', 'allow_comments')
        
