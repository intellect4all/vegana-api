from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.Home, name='home' ),
    path('<slug>/', views.Product, name='product' )
    
]