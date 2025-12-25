from django.shortcuts import render, get_object_or_404
from urllib3 import request
from .models import Producto, Categoria, Pedido
from .forms import PedidoForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.shortcuts import render
from appTienda.models import Pedido
from django.utils.dateparse import parse_date

def index(request):
    return render(request, 'base.html')


def catalogo(request):
    query = request.GET.get('search', '')
    if query:
        productos= Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
        categorias= Categoria.objects.filter()
    else:
        productos= Producto.objects.all()
        categorias= Categoria.objects.all()

    data = {
        'productos': productos,
        'categorias': categorias,
        'query': query
        }

    return render(request, 'catalogo/catalogo.html', data)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()

    data = {
        'producto': producto,
        'categorias': categorias
    }

    return render(request, 'catalogo/detalle_producto.html', data)


def realizar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.origen_pedido = 'SITIO_WEB'
            pedido.estado_pedido = 'SOLICITADO'
            pedido.estado_pago = 'PENDIENTE'
            pedido.save() 
            
            messages.success(request, f'¡Pedido realizado con éxito! Tu token de seguimiento es: {pedido.token}')
            
            return redirect('seguimiento_pedido', token=pedido.token)
    else:
        form = PedidoForm()

    return render(request, 'catalogo/realizar_pedido.html', {'form': form})

def examinar_pedido(request):
    pedido = Pedido.objects.all()
    data = {'pedido': pedido}
    return render(request, 'catalogo/estado_pedido.html', data)

def seguimiento_pedido(request, token):
    pedido = get_object_or_404(Pedido, token=token)
    

    estados_posibles = [choice[1] for choice in Pedido.ESTADO_PEDIDO]  
    chart_labels = estados_posibles
    chart_data = [1 if choice == pedido.get_estado_pedido_display() else 0 for choice in estados_posibles]  

    context = {
        'pedido': pedido,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'catalogo/estado_pedido.html', context)


def reporte_pedidos(request):
    # Filtros
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    estado = request.GET.get('estado')
    plataforma = request.GET.get('plataforma')

    pedidos = Pedido.objects.all()

    if desde:
        pedidos = pedidos.filter(fecha_solicitada__date__gte=parse_date(desde))
    if hasta:
        pedidos = pedidos.filter(fecha_solicitada__date__lte=parse_date(hasta))
    if estado:
        pedidos = pedidos.filter(estado_pedido=estado)
    if plataforma:
        pedidos = pedidos.filter(origen_pedido=plataforma)

    # Métricas
    por_estado = pedidos.values('estado_pedido').annotate(cantidad=Count('estado_pedido')).order_by('-cantidad')
    por_plataforma = pedidos.values('origen_pedido').annotate(cantidad=Count('origen_pedido')).order_by('-cantidad')
    productos_solicitados = pedidos.values('producto_referencia__nombre').annotate(cantidad=Count('producto_referencia')).order_by('-cantidad')[:10]


    labels_estado = [item['estado_pedido'] for item in por_estado]
    data_estado = [item['cantidad'] for item in por_estado]


    labels_plataforma = [item['origen_pedido'] for item in por_plataforma]
    data_plataforma = [item['cantidad'] for item in por_plataforma]

    context = {
        'pedidos': pedidos,
        'por_estado': por_estado,
        'por_plataforma': por_plataforma,
        'productos_solicitados': productos_solicitados,
        'labels_estado': labels_estado,
        'data_estado': data_estado,
        'labels_plataforma': labels_plataforma,
        'data_plataforma': data_plataforma,
        'desde': desde,
        'hasta': hasta,
        'estado': estado,
        'plataforma': plataforma,
        'estados_choices': Pedido.ESTADO_PEDIDO,
        'plataformas_choices': Pedido.ORIGEN_PEDIDO,
    }
    return render(request, 'catalogo/reporte_pedidos.html', context)