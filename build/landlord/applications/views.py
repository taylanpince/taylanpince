from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from applications.forms import TenantApplicationForm


def application_form(request):
    """
    Renders and processes the application form
    """
    if request.method == "POST":
        form = TenantApplicationForm(request.POST, auto_id="%s", prefix="TenantApplicationForm")
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse("application_complete"))
    else:
        form = TenantApplicationForm(auto_id="%s", prefix="TenantApplicationForm")
    
    return render_to_response("applications/form.html", {
        "form": form,
    }, context_instance=RequestContext(request))
