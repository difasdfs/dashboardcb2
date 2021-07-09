from django.urls import path, include
from . import views

urlpatterns = [
    path('data_sold_percabang', views.data_sold_percabang, name='data_sold_percabang'),
    path('data_sold/', views.data_sold, name="data_sold"),
    path('sku/', views.sku, name="sku"),
    path('update_sku/', views.update_sku, name="update_sku"),
    path('kategori/', views.kategori, name="kategori"),
]