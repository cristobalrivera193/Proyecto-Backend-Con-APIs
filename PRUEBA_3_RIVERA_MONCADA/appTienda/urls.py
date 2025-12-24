# apptienda/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('catalogo/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
]