from django import template
import re

register = template.Library()

@register.filter
def is_external(href):
    external_re = re.compile(r'http(s)?://.*')
    return re.match(external_re, href)
