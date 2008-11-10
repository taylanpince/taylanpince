from django.forms import ModelForm

from applications.models import TenantApplication


class TenantApplicationForm(ModelForm):
    """
    A form for creating a new tenant application
    """
    class Meta:
        model = TenantApplication
        exclude = ("reviewed",)
