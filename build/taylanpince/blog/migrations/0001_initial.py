from django.db import models
from django.utils.translation import ugettext_lazy as _

from south.db import db

from blog.models import *


class Migration:
    
    def forwards(self):
        
        # Model 'Category'
        db.create_table('blog_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=100)),
            ('slug', AutoSlugField(_("Slug"), populate_from="title")),
        ))
        # Model 'PostType'
        db.create_table('blog_posttype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=100)),
            ('slug', AutoSlugField(_("Slug"), populate_from="title")),
            ('icon', models.ImageField(_("Icon"), upload_to="files/blog/icons", blank=True, null=True)),
        ))
        
        # Mock Models
        PostType = db.mock_model(model_name='PostType', db_table='blog_posttype', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Post'
        db.create_table('blog_post', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('teaser', models.TextField(_("Teaser"), blank=True)),
            ('body', models.TextField(_("Body"), blank=True)),
            ('link', models.URLField(_("Link"), blank=True, null=True, verify_exists=True)),
            ('tags', TagField()),
            ('type', models.ForeignKey(PostType, verbose_name=_("Type"))),
            ('creation_date', CreateDateTimeField(_("Creation Date"), editable=True)),
            ('change_date', ChangeDateTimeField(_("Change Date"))),
            ('published', models.BooleanField(_("Published"), default=True)),
            ('slug', AutoSlugField(_("Slug"), populate_from="title")),
        ))
        # Mock Models
        Post = db.mock_model(model_name='Post', db_table='blog_post', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        Category = db.mock_model(model_name='Category', db_table='blog_category', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # M2M field 'Post.categories'
        db.create_table('blog_post_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(Post, null=False)),
            ('category', models.ForeignKey(Category, null=False))
        )) 
        
        # Mock Models
        Post = db.mock_model(model_name='Post', db_table='blog_post', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Comment'
        db.create_table('blog_comment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('body', models.TextField(_("Comment"))),
            ('author', models.CharField(_("Name"), blank=True, max_length=255)),
            ('email', models.EmailField(_("Email"), blank=True)),
            ('url', models.URLField(_("Web Site"), blank=True, verify_exists=True)),
            ('ip_address', models.IPAddressField(_("IP Address"), blank=True, null=True)),
            ('post', models.ForeignKey(Post, verbose_name=_("Post"))),
            ('creation_date', CreateDateTimeField(_("Creation Date"), editable=True)),
            ('change_date', ChangeDateTimeField(_("Change Date"))),
            ('published', models.BooleanField(_("Published"), default=False)),
        ))
        
        db.send_create_signal('blog', ['Category','PostType','Post','Comment'])
    
    def backwards(self):
        db.delete_table('blog_comment')
        db.delete_table('blog_post_categories')
        db.delete_table('blog_post')
        db.delete_table('blog_posttype')
        db.delete_table('blog_category')
        
