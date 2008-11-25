from django import forms
from django.utils.translation import ugettext_lazy as _

from blog.models import Comment


class CommentForm(forms.ModelForm):
    """
    A comment form
    """
    remember = forms.BooleanField(label=_("Remember me"), required=False)
    
    class Meta:
        model = Comment
        exclude = ("ip_address", "creation_date", "change_date", "published", "post")
