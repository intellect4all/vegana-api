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


# Register your models here.
