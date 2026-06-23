from django.db import models
from django.contrib.auth.models import AbstractUser

# usuario
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username    



# categorias
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Disponible para la venta")

    def __str__(self):
        return self.nombre


# tales
class Talle(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Talle")
    activo = models.BooleanField(default=True, verbose_name="Disponible para la venta")

    def __str__(self):
        return self.nombre


#producto
class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos", verbose_name="Categoría")
    descripcion = models.TextField(verbose_name="Descripción")
    talles = models.ManyToManyField(Talle, related_name="productos", verbose_name="Talles Disponibles", blank=True)
    imagen = models.ImageField(upload_to='productos/', verbose_name="Imagen del Producto")
    es_talle_unico = models.BooleanField(default=False, verbose_name="¿Es Talle Único?")
    activo = models.BooleanField(default=True, verbose_name="Disponible para la venta")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    


# para el stock por talle
class VarianteProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    talle = models.ForeignKey(Talle, on_delete=models.PROTECT, related_name="variantes")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock para este talle")

    class Meta:
        unique_together = ('producto', 'talle') # Evita duplicar el talle para un mismo producto

    def __str__(self):
        return f"{self.producto.nombre} - Talle: {self.talle.nombre} (Stock: {self.stock})"

# pedido
CHOICES_ESTADO = [
    ('PENDIENTE', 'Pendiente de Pago'),
    ('PAGADO', 'Pagado'),
    ('ENVIADO', 'Enviado'),
    ('ENTREGADO', 'Entregado'),
    ('CANCELADO', 'Cancelado'),
]


# detalle del pedido
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos", verbose_name="Cliente")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total ($)")
    estado = models.CharField(max_length=20, choices=CHOICES_ESTADO, default='PENDIENTE', verbose_name="Estado")
    direccion_entrega = models.CharField(max_length=255, verbose_name="Dirección de Envío")

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles", verbose_name="Pedido")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    talle_comprado = models.CharField(max_length=10, verbose_name="Talle Comprado")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario ($)")

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Talle {self.talle_comprado})"