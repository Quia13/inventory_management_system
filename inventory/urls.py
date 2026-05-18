from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('app/inventory', views.inventory, name='inventory'),

    path('app/inventory/product', views.product, name='product'),
    path('app/products/add', views.add_product, name='product.add'),
    path('app/products/<int:id>/update', views.update_product, name='product.update'),
    path('app/products/<int:id>/delete', views.delete_product, name='product.delete'),
]