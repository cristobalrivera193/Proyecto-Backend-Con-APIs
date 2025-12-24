from django.urls import path
from .api_views import InsumoViewSet, PedidoCreateUpdate, PedidoFiltrar

urlpatterns = [
    path('insumos/', InsumoViewSet.as_view({'get': 'list', 'post': 'create'}), name='insumos-list'),
    path('insumos/<int:pk>/', InsumoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='insumos-detail'),
    path('pedidos/', PedidoCreateUpdate.as_view(), name='pedidos-create-update'),
    path('pedidos/filtrar/', PedidoFiltrar.as_view(), name='pedidos-filtrar'),
]