from django import template
from django.http import request
from store.models import Order, Wishlist

register= template.Library()

@register.filter
def cart_item_count(user):
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        return order.items.count()
    else:
        return 0
     
@register.filter
def wishlist_item_count(user):
    wishlist_qs = Wishlist.objects.filter(user=user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        return wishlist.items.count()
    else:
        return 0
     