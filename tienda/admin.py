from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Usuario, Categoria, Talle, Producto, Pedido, DetallePedido, VarianteProducto
from django.utils.safestring import mark_safe
# Register your models here.

#config del user
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ['username', 'email', 'first_name', 'last_name', 'telefono', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefono']


    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'direccion')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('telefono', 'direccion','first_name', 'last_name', 'email')}),
    )

# para cargar talles y stocks directamente en el producto
class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1 #una fila vacia para agregar un talle
    readonly_fields = ['stock','talle'] 


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    fields = ['producto', 'cantidad', 'precio_unitario',]
    readonly_fields = ['precio_unitario']
    @admin.display(description='Subtotal')
    def calcular_subtotal(self, obj):
        """Calcula dinámicamente el subtotal de la línea para el administrador"""
        if obj.id and obj.cantidad and obj.precio_unitario:
            return f"${obj.cantidad * obj.precio_unitario}"
        return "$0"
    
#config de productos
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'es_talle_unico', 'activo', 'estado_visual', 'fecha_creacion')
    list_filter = ['activo', 'categoria', 'es_talle_unico', 'fecha_creacion'] # Filtros
    search_fields = ['nombre', 'descripcion', 'categoria__nombre'] # Buscador
    ordering = ['-fecha_creacion'] #mas nuevos primero
    inlines = [VarianteProductoInline] # Para gestionar talles y stock desde el admin del producto
    actions = ['activar_productos', 'desactivar_productos'] #acciones personalizadas

    @admin.display(description='Estado')
    def estado_visual(self, obj):
        """Muestra un badge de color nativo para el borrado lógico"""
        if obj.activo:
            return mark_safe('<span style="color: #28a745; font-weight: bold;">● Activo</span>')
        return mark_safe('<span style="color: #dc3545; font-weight: bold;">● Inactivo</span>')
    
    @admin.action(description='Desactivar productos seleccionados (Borrado Lógico)')
    def desactivar_productos(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, "Los productos seleccionados se ocultaron del catálogo.")

    @admin.action(description='Activar productos seleccionados')
    def activar_productos(self, request, queryset):
        queryset.update(activo=True)
        self.message_user(request, "Los productos seleccionados se volvieron a activar.")


# config de pedidos
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha', 'total', 'estado_badge', 'direccion_entrega']
    list_filter = ['estado', 'fecha']
    search_fields = ['usuario__username', 'usuario__first_name', 'direccion_entrega', 'id']
    ordering = ['-fecha']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha']

    @admin.display(description='Total')
    def total_formateado(self, obj):
        return f"${obj.total}"

    @admin.display(description='Estado del Pedido')
    def estado_badge(self, obj):
        # badge de color para cada estado de pedido
        colores = {
            'pendiente': '#ffc107',
            'pagado': '#28a745',
            'cancelado': '#dc3545',
            'entregado': '#17a2b8'
        }
        color = colores.get(obj.estado.lower(), '#6c757d')
        return mark_safe(f'<strong style="color: {color}; text-transform: uppercase;">{obj.estado}</strong>')

# config de categorias
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    actions = ['activar_categorias', 'desactivar_categorias']

    @admin.action(description='Desactivar categorías seleccionadas')
    def desactivar_categorias(self, request, queryset):
        queryset.update(activo=False)

    @admin.action(description='Activar categorías seleccionadas')
    def activar_categorias(self, request, queryset):
        queryset.update(activo=True)

@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

admin.site.register(Usuario, CustomUserAdmin)