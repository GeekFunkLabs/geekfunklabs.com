from django import template
from django.utils.safestring import mark_safe

from core.utils import render_markdown

register = template.Library()


@register.filter
def markdown(text):
    return mark_safe(render_markdown(text))
