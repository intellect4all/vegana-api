from store.views import CategoryView
from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    path('products/', ProductListApiView.as_view(), name="products" ),
    path('products/<slug>/', ProductDetailView.as_view(), name="products-details" ),
    path('test/', TestApiView.as_view()),
    path('categories/', CategoriesView.as_view(), name="categories" ),
    path('categories/<category>/', CategoryPostsView.as_view(), name="category-products" ),
]
