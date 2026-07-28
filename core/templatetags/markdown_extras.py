from django import template
from django.utils.safestring import mark_safe
from markdown_it import MarkdownIt

register = template.Library()

md = MarkdownIt("commonmark")

@register.filter
def render_markdown(text):
    return mark_safe(md.render(text))
