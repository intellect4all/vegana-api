from django import template
from django.http import request
from store.models import Order

register= template.Library()

@register.filter
def cart_item_count(user):
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        return order.items.count()
    else:
        return 0
     
