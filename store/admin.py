from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('name', 'actual_price', 'is_on_sale', 'created', 'slug')
    list_filter = ('created', 'is_on_sale', 'category', 'tags')
    
    search_fields = ('name',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for Tag'''

    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    '''Admin View for OrderItem'''
    list_display = ('user', 'ordered', 'product', 'quantity')
    list_filter = ('ordered',)
    search_fields = ('user',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''
    list_display = ('user', 'ordered')
    list_filter = ('ordered',  'date_created')
    search_fields = ('user',)
    
@admin.register(Wishlist)
class WishListAdmin(admin.ModelAdmin):
    '''Admin View for WishList'''

    list_display = ('user', 'ordered')
    list_filter = ('ordered', 'date_created')
    search_fields = ('user',)