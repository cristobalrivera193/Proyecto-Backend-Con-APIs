from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido
from .forms import PedidoForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q


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
    
    context = {
        'pedido': pedido,
    }
    return render(request, 'catalogo/estado_pedido.html', context)
