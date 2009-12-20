from django.db import models
from django.utils.translation import ugettext_lazy as _

from south.db import db

from portfolio.models import *


class Migration:
    def forwards(self):
        # Model 'Category'
        db.create_table('portfolio_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('slug', AutoSlugField(_("Slug"), populate_from="title")),
        ))
        
        # Mock Models
        Piece = db.mock_model(model_name='Piece', db_table='portfolio_piece', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Photo'
        db.create_table('portfolio_photo', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('image', models.ImageField(_("Image"), upload_to="files/portfolio")),
            ('piece', models.ForeignKey(Piece, verbose_name=_("Piece"))),
        ))
        
        # Model 'Piece'
        db.create_table('portfolio_piece', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('teaser', models.TextField(_("Teaser"), blank=True)),
            ('body', models.TextField(_("Body"), blank=True)),
            ('link', models.URLField(_("Link"), blank=True, null=True, verify_exists=True)),
            ('slug', AutoSlugField(_("Slug"), populate_from="title")),
            ('published', models.BooleanField(_("Published"), default=True)),
            ('creation_date', CreateDateTimeField(_("Creation Date"), editable=True)),
        ))
        
        # Mock Models
        Piece = db.mock_model(model_name='Piece', db_table='portfolio_piece', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        Category = db.mock_model(model_name='Category', db_table='portfolio_category', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # M2M field 'Piece.categories'
        db.create_table('portfolio_piece_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(Piece, null=False)),
            ('category', models.ForeignKey(Category, null=False))
        )) 
        
        db.send_create_signal('portfolio', ['Category','Photo','Piece'])
    
    def backwards(self):
        db.delete_table('portfolio_piece_categories')
        db.delete_table('portfolio_piece')
        db.delete_table('portfolio_photo')
        db.delete_table('portfolio_category')
