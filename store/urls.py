from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.HomePage, name='home' ),
    path("cart/", views.Cart, name="cart"),
    path('products/<slug>/', views.ProductDetails, name='product' ),
    path("category/<category>/", views.CategoryView, name="category"),
    path('add_to_cart/<slug>/', views.add_to_cart, name="add-to-cart"),
    
]