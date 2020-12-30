from django.db.models import fields
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, Serializer
from rest_framework import serializers
from store.models import *

class ProductSerializer(ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    class Meta:
        model = Product
        fields = ('url','name', 'actual_price', 'discount_price', 'category', 'tags', 'description', 'featured_image', 'created', 'shipping_fee', )

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class OrderItemSerializer(Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    ordered = serializers.BooleanField()