from enum import auto
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)

class Tag(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=150)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.ManyToManyField('category', related_name='category', default='Uncategorized')
    tags = models.ManyToManyField('category', related_name='tags', blank=True)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(max_length=3000)
    featured_image = models.ImageField(null=True, blank=True)


    #this returns the slug of the product
    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)           # add this
        super().save(*args, **kwargs)                                 # add this


# Create your models here.
