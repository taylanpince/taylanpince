import re

from django import template


register = template.Library()


@register.simple_tag
def active_path(request, path, style="active"):
    """
    Returns a modifiable string `style` (active by default) if the given path 
    is at the beginning of the current request.path
    """
    if re.search(path, request.path):
        return style
    else:
        return ""


@register.filter
def smartypants(value):
    """
    Filters the value through SmartyPants for converting plain 
    ASCII punctuation characters into typographically correct versions
    """
    try:
        from smartypants import smartyPants
        
        return smartyPants(value)
    except ImportError:
        return value
