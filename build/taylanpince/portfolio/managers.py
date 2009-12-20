from django.db import models


class PieceManager(models.Manager):
    """
    Lists only published portfolio pieces
    """
    def get_query_set(self):
        return super(PieceManager, self).get_query_set().filter(published=True).order_by("-creation_date")
