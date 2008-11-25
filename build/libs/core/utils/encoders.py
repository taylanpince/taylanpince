import types

from decimal import *

from django.db import models
from django.utils import simplejson
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.core.serializers.json import DateTimeAwareJSONEncoder


class LazyEncoder(simplejson.JSONEncoder):
    """
    Convert lazy translations before being passed on to simplejson's encoder
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj


def convert_object_to_json(object, fields=[], raw=False):
    """
    Convert a Model instance into a JSON dictionary by only including the 
    specified fields - this allows us to include custom properties and get 
    rid of unnecessary data given by the default json encoder
    """
    data = {}
    
    if len(fields) > 0:
        for field in fields:
            data[field] = getattr(item, field)
    else:
        for field in item._meta.fields:
            data[field.attname] = getattr(item, field.attname)
    
    if raw:
        return data
    else:
        return simplejson.dumps(data, cls=DateTimeAwareJSONEncoder, ensure_ascii=False)


def convert_queryset_to_json(queryset, fields=[]):
    """
    Convert a QuerySet into a JSON dictionary by only including the specified
    fields - this allows us to include custom properties and get rid of 
    unnecessary data given by the default json encoder
    """
    output = []
    
    for item in queryset:
        output.append(convert_object_to_json(item, fields, True))
    
    return simplejson.dumps(output, cls=DateTimeAwareJSONEncoder, ensure_ascii=False)
