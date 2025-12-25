from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('catalogo/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('examinar_pedido/', views.examinar_pedido, name='examinar_pedido'),
    path('seguimiento/<str:token>/', views.seguimiento_pedido, name='seguimiento_pedido'),
    path('api/', include('appTienda.api_urls')),
    path('reporte/', views.reporte_pedidos, name='reporte_pedidos'),
]