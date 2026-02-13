from django import template

register = template.Library()

@register.filter(name='chr')
def to_char(value):
    return chr(int(value))

