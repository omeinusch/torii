from django import template
from django.utils.safestring import mark_safe
from markdown2 import markdown as markdown2

register = template.Library()

@register.filter()
def markdown(content):
    return mark_safe(markdown2(content))