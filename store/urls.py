from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.HomePage, name='home' ),
    path('<slug>/', views.ProductDetails, name='product' ),
    path("category/<category>/", views.CategoryView, name="category")
    
]