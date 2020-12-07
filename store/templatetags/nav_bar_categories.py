from django import template
from store.models import Category

register= template.Library()

@register.filter
def categories():
    categories = Category.objects.all()[0]
    return categories
