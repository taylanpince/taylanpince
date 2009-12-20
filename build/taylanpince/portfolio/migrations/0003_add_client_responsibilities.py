from django.db import models
from django.utils.translation import ugettext_lazy as _

from south.db import db

from portfolio.models import *


class Migration:
    def forwards(self):
        # Adding field 'Piece.client'
        db.add_column('portfolio_piece', 'client', models.CharField(_("Client"), blank=True, max_length=255, default=""), keep_default=False)
        
        # Adding field 'Piece.responsibilities'
        db.add_column('portfolio_piece', 'responsibilities', models.TextField(_("Responsibilities"), blank=True, default=""), keep_default=False)
    
    def backwards(self):
        # Deleting field 'Piece.client'
        db.delete_column('portfolio_piece', 'client')
        
        # Deleting field 'Piece.responsibilities'
        db.delete_column('portfolio_piece', 'responsibilities')
