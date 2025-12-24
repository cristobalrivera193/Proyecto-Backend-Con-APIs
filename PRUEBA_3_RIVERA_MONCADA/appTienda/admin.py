from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto, Insumo, Pedido

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    list_filter = ['nombre']
    search_fields = ['nombre']
    prepopulated_fields = {"slug": ["nombre"]}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'descripcion', 'precio_base', 'vista_imagen']
    list_filter = ['nombre']
    search_fields = ['nombre', 'categoria__nombre']
    prepopulated_fields = {"slug": ["nombre"]}
    def vista_imagen(self, obj):
        
        if obj.imagen:
            return format_html('<img src="{}" width="60" style="border-radius:6px;" />', obj.imagen.url)
        return "Sin imagen"     

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'cantidad', 'marca', 'color']
    prepopulated_fields = {"slug": ["nombre"]}

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'origen_pedido', 'estado_pago', 'estado_pedido', 'email', 'imagen_Referencia']
