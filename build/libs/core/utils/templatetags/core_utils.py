import re

from django import template


register = template.Library()


@register.simple_tag
def active_path(request, path, class="active"):
    """
    Returns a modifiable string `class` (active by default) if the given path 
    is at the beginning of the current request.path
    """
    if re.search(path, request.path):
        return class
    else:
        return ""
