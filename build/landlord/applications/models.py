from django.db import models
from django.utils.translation import ugettext_lazy as _


class TenantApplication(models.Model):
    """
    A tenant application that contains contact, employment and residency info
    of the applicant
    """
    
    BOOLEAN_CHOICES = (
        (False, _("No")),
        (True, _("Yes")),
    )
    
    # Contact Information
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=20, help_text=_("Preferably your mobile phone."))
    email = models.EmailField(_("Email Address"))
    # Personal
    income = models.CharField(_("Yearly Income"), max_length=100)
    pets = models.BooleanField(_("Will there be pets in the household?"), default=False, choices=BOOLEAN_CHOICES)
    smokers = models.BooleanField(_("Will there be smokers in the household?"), default=False, choices=BOOLEAN_CHOICES)
    # Current Residence
    landlord_name = models.CharField(_("Landlord's Name"), max_length=150)
    landlord_phone = models.CharField(_("Landlord's Phone Number"), max_length=20)
    tenancy_start_date = models.DateField(_("Tenancy Start Date"))
    # Previous Residence
    prev_landlord_name = models.CharField(_("Landlord's Name"), max_length=150, blank=True)
    prev_landlord_phone = models.CharField(_("Landlord's Phone Number"), max_length=20, blank=True)
    prev_tenancy_start_date = models.DateField(_("Tenancy Start Date"), blank=True, null=True)
    # Employment
    employer = models.CharField(_("Employer"), max_length=100)
    employer_reference_name = models.CharField(_("Reference's Name"), max_length=150)
    employer_reference_phone = models.CharField(_("Reference's Phone Number"), max_length=20)
    employment_start_date = models.DateField(_("Employment Start Date"))
    # Timestamp & Flags
    application_date = models.DateTimeField(_("Application Date"), editable=False, auto_now_add=True)
    reviewed = models.BooleanField(_("Reviewed"), default=False)
    
    class Meta:
        verbose_name = _("Tenant Application")
        verbose_name_plural = _("Tenant Applications")
    
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
