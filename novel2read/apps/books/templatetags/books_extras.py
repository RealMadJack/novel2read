from django import template

register = template.Library()


@register.filter(name='ifinlist')
def ifinlist(value, list):
    return True if value in list else False
