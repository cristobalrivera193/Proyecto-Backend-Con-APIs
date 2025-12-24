from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria
from .forms import PedidoForm
from django.shortcuts import redirect


def index(request):
    return render(request, 'base.html')


def catalogo(request):
    productos= Producto.objects.all()
    categorias= Categoria.objects.all()

    data = {
        'productos': productos,
        'categorias': categorias
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
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = PedidoForm()
        
    data = {
        'form': form
    }
    return render(request, 'catalogo/realizar_pedido.html', data)