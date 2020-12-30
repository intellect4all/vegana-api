from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import *
from .serializers import *

class ProductListApiView(ListAPIView):
    queryset = Product.objects.filter(is_on_sale=True)
    serializer_class = ProductSerializer

class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(is_on_sale=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryPostsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Product.objects.filter(category__name=category.title(), is_on_sale=True)

class TestApiView(APIView):
    def get(self, request, format=None):
        items = OrderItem.objects.filter(user=request.user, ordered=True)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)
