from datetime import datetime

from django.db import models


class PostManager(models.Manager):
    """
    Lists only published posts
    """
    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(published=True).order_by("-creation_date")


class CommentManager(models.Manager):
    """
    Lists only published comments
    """
    def get_query_set(self):
        return super(CommentManager, self).get_query_set().filter(published=True).order_by("creation_date")
