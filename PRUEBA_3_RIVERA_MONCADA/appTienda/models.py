from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    descripcion = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField()
    descripcion = models.TextField(max_length=250, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    precio_base = models.IntegerField()
    imagen = models.ImageField(upload_to='productos', blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField()
    tipo = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='insumo')
    cantidad = models.PositiveIntegerField()
    marca = models.CharField(max_length=50) 
    color = models.CharField(max_length=50)

class Pedido(models.Model):
    
    ESTADO_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('PAGADO', 'Pagado'),
    ]
    ESTADO_PEDIDO = [
        ('SOLICITADO', 'Solicitado'),
        ('APROBADO', 'Aprobado'),
        ('EN_PROCESO', 'En proceso'),
        ('REALIZADA', 'Realizada'),
        ('ENTREGADA', 'Entregada'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    ORIGEN_PEDIDO = [
        ('FACEBOOK', 'Facebook'),
        ('INSTAGRAM', 'Instagram'),
        ('WHATSAPP', 'WhatsApp'),
        ('SITIO_WEB', 'Sitio Web'),
        ('Presencial', 'Presencial'),
    ]
    token = models.CharField(max_length=12, unique=True)
    cliente_nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    email = models.CharField(max_length=200)
    producto_referencia = models.ForeignKey('Producto', on_delete=models.PROTECT, related_name='pedido', null=True, blank=True)
    imagen_Referencia = models.ImageField(upload_to='productos', blank=True)
    fecha_solicitada = models.DateTimeField(auto_now_add=True)
    origen_pedido = models.CharField(choices=ORIGEN_PEDIDO, default='SITIO_WEB')
    estado_pago = models.CharField(choices=ESTADO_PAGO, default='PENDIENTE')
    estado_pedido = models.CharField(choices=ESTADO_PEDIDO, default='SOLICITADO')

    def __str__(self):
        return f"Pedido {self.token}"

