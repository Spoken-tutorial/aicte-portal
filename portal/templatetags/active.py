import re

from django import template

register = template.Library()

def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

register.simple_tag(active)
