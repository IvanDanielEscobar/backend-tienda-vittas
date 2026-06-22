from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Categoria, Talle, Producto, Pedido, DetallePedido, VarianteProducto
# Register your models here.

#config del user
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'first_name', 'last_name', 'telefono', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'direccion')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'direccion')}),
    )

# para cargar talles y stocks directamente en el producto
class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1 #una fila vacia para agregar un talle


#filtros y busquedas en productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'es_talle_unico', 'activo', 'fecha_creacion')
    list_filter = ['activo', 'categoria', 'es_talle_unico'] # Filtros
    search_fields = ['nombre', 'descripcion'] # Buscador
    ordering = ['-fecha_creacion'] #mas nuevos primero
    inlines = [VarianteProductoInline] # Para gestionar talles y stock desde el admin del producto

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['usuario__username', 'direccion_entrega']
    ordering = ['-fecha']
    inlines = [DetallePedidoInline]

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Talle)