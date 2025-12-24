from datetime import datetime
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from .models import Insumo, Pedido
from .serializers import InsumoSerializer, PedidoSerializer  # Crea serializers.py

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoCreateUpdate(generics.GenericAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            pedido = Pedido.objects.get(pk=pk)
        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PedidoFiltrar(generics.ListAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Pedido.objects.all()
        desde = self.request.query_params.get('desde_fecha')
        hasta = self.request.query_params.get('hasta_fecha')
        estado = self.request.query_params.get('estado')
        max_resultados = self.request.query_params.get('max_resultados', 10)

        if desde and hasta:
            queryset = queryset.filter(fecha_solicitada__range=[desde, hasta])
        if estado:
            queryset = queryset.filter(estado_pedido=estado)
        return queryset[:int(max_resultados)]
    
from rest_framework.exceptions import ValidationError

def get_queryset(self):
    # ... código anterior ...
    try:
        max_resultados = int(max_resultados)
        if max_resultados > 50 or max_resultados < 1:
            raise ValidationError({'max_resultados': 'Debe estar entre 1 y 50'})
    except ValueError:
        raise ValidationError({'max_resultados': 'Debe ser un número'})

    try:
        datetime.strptime(desde, '%Y-%m-%d') if desde else None
        datetime.strptime(hasta, '%Y-%m-%d') if hasta else None
    except ValueError:
        raise ValidationError({'fechas': 'Formato YYYY-MM-DD inválido'})

    if estado and estado not in dict(Pedido.ESTADO_PEDIDO).keys():
        raise ValidationError({'estado': 'Estado inválido'})

    return queryset[:max_resultados]