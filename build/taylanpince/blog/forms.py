from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    """
    A comment form
    """
    class Meta:
        model = Comment
        exclude = ("ip_address", "creation_date", "change_date", "published", "post")
