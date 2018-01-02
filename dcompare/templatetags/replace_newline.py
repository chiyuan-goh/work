from django import template

register  = template.Library()

@register.filter
def replace_newline(txt):
    return txt.replace("\n", "</p><p>")