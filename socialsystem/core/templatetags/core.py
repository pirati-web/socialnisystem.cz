from django import template
from django.template import Context, Template
import re

from socialsystem.markdown import markdownify

register = template.Library()

@register.filter
def is_external(href):
    external_re = re.compile(r'http(s)?://.*')
    return re.match(external_re, href)


@register.simple_tag(takes_context=True)
def render_html(context, template_str):
    template = Template('{%% load webpack_static from webpack_loader %%}%s' % template_str)
    return template.render(context)
