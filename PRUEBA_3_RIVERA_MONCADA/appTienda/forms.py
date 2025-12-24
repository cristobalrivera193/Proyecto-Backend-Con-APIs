
from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['token', 'cliente_nombre','descripcion', 'email', 'producto_referencia', 'imagen_Referencia' ]
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'email': forms.Textarea(attrs={'class': 'form-control', 'rows':3}), 
            #'producto_referencia': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            #'imagen_Referencia':#
        }
        labels = {
            'cliente_nombre': 'Nombre del Cliente',
            'email': 'Email que realiza el pedido',
            'descripcion': 'Descripción de lo solicitado',
            'producto_referencia': 'Producto Referencia',
            'imagen_Referencia': 'Imagen Referencia',
            'usuario': 'Usuario que realiza el pedido',
        }