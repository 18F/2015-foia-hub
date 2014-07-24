from django import template
register = template.Library()

@register.filter('object_class')
def field_class(ob):
    return ob.__class__.__name__