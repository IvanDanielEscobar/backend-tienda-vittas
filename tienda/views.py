
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Producto, Categoria, Talle, Pedido, DetallePedido
from .forms import EmpleadoForm, RegistroUsuarioForm, ProductoForm
from .serializers import ProductoSerializer, CategoriaSerializer
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

Usuario = get_user_model()
# Create your views here.
# Inicio
class CatalogoView(ListView):
    model = Producto
    template_name = 'tienda/catalogo.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        # Solo productos activos
        queryset = Producto.objects.filter(activo=True)
        # Permite filtrar por categoria desde la URL si existe (ej. ?categoria=1)
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

# Detalle de una Prenda
class ProductoDetalleView(DetailView):
    model = Producto
    template_name = 'tienda/detalle_producto.html'
    context_object_name = 'producto'

# Registro de Usuario
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Lo logueamos automáticamente al registrarse
            messages.success(request, "¡Registro exitoso! Bienvenido a Vittas.")
            return redirect('catalogo')
        else:
            messages.error(request, "Hubo un error en el formulario. Por favor, verificalo.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'tienda/registro.html', {'form': form})

# CRUD de Productos
class CrearProductoView(PermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/form_producto.html'
    success_url = reverse_lazy('panel_productos')
    permission_required = 'tienda.add_producto'

    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)
    

class PanelProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'tienda/crud_productos.html'
    context_object_name = 'productos'
    ordering = ['-fecha_creacion']

class EditarProductoView(PermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'tienda/form_producto.html' 
    success_url = reverse_lazy('panel_productos')
    permission_required = 'tienda.change_producto'

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente.")
        return super().form_valid(form)

class BorrarProductoView(PermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'tienda/confirmar_borrado.html' 
    success_url = reverse_lazy('panel_productos')
    permission_required = 'tienda.delete_producto'

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.activo = False # <-- BORRADO LÓGICO
        self.object.save()
        messages.success(self.request, "Producto desactivado del catálogo con éxito.")
        return redirect(self.get_success_url())
#CRUD de Categorías 
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'tienda/crud_categorias.html'
    context_object_name = 'categorias'

class CategoriaCreateView(PermissionRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'tienda/form_categoria.html'
    success_url = reverse_lazy('crud_categorias')
    permission_required = 'tienda.add_categoria'

class CategoriaUpdateView(PermissionRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'tienda/form_categoria.html'
    success_url = reverse_lazy('crud_categorias')
    permission_required = 'tienda.change_categoria'

class CategoriaDeleteView(PermissionRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'tienda/confirmar_borrado.html'
    success_url = reverse_lazy('crud_categorias')
    permission_required = 'tienda.delete_categoria'

    def form_valid(self, form):
        self.object = self.get_object()
        if hasattr(self.object, 'activo'):
            self.object.activo = False  # <-- BORRADO LÓGICO
            self.object.save()
            messages.success(self.request, "Categoría desactivada con éxito.")
        else:
            messages.warning(self.request, "Esta categoría no tiene un campo 'activo'. No se pudo desactivar.")
        return redirect(self.get_success_url())
    
# CRUD de talles

class TalleListView(LoginRequiredMixin, ListView):
    model = Talle
    template_name = 'tienda/crud_talles.html'
    context_object_name = 'talles'

class TalleCreateView(PermissionRequiredMixin, CreateView):
    model = Talle
    fields = ['nombre']
    template_name = 'tienda/form_talle.html'
    success_url = reverse_lazy('crud_talles')
    permission_required = 'tienda.add_talle'

class TalleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Talle
    fields = ['nombre']
    template_name = 'tienda/form_talle.html'
    success_url = reverse_lazy('crud_talles')
    permission_required = 'tienda.change_talle'

class TalleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Talle
    template_name = 'tienda/confirmar_borrado.html'
    success_url = reverse_lazy('crud_talles')
    permission_required = 'tienda.delete_talle'

    def form_valid(self, form):
        self.object = self.get_object()
        if hasattr(self.object, 'activo'):
            self.object.activo = False  # <-- BORRADO LÓGICO
            self.object.save()
            messages.success(self.request, "Talle desactivado con éxito.")
        else:
            messages.warning(self.request, "Este talle no tiene un campo 'activo'. No se pudo desactivar.")
        return redirect(self.get_success_url())
    


# crud empleados
class SuperuserRequiredMixin(PermissionRequiredMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class ListarEmpleadosView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = Usuario
    template_name = 'tienda/crud_empleados.html'
    context_object_name = 'empleados'
    permission_required = 'tienda.view_usuario'

    def get_queryset(self):
        # Filtramos para no mostrar clientes ni a vos mismo en la lista de empleados
        return Usuario.objects.filter(is_staff=True).exclude(id=self.request.user.id)

class CrearEmpleadoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Usuario 
    form_class = EmpleadoForm
    template_name = 'tienda/form_empleado.html'
    success_url = reverse_lazy('panel_productos')
    permission_required = 'tienda.add_usuario'
    
    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, "Cuenta de empleado Vittas creada con éxito.")
        return super().form_valid(form)
    

class EditarEmpleadoView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Usuario
    form_class = EmpleadoForm
    template_name = 'tienda/form_empleado.html' # Reutiliza el mismo template limpio de alta
    success_url = reverse_lazy('crud_empleados')
    permission_required = 'tienda.change_usuario'

    def form_valid(self, form):
        messages.success(self.request, "Legajo de empleado actualizado correctamente.")
        return super().form_valid(form)


class BorrarEmpleadoView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Usuario
    fields = []
    template_name = 'tienda/confirmar_borrado.html'
    success_url = reverse_lazy('crud_empleados')
    permission_required = 'tienda.delete_usuario'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False  # <-- DESACTIVACION LOGICA
        self.object.save()
        messages.success(request, f"La cuenta de {self.object.username} fue dada de baja del sistema.")
        return redirect(self.success_url)

# API
# Listar los productos o filtrar por categoría 
@api_view(['GET'])
def api_productos(request):
    productos = Producto.objects.filter(activo=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

# Detalle de un producto por ID
@api_view(['GET'])
def api_producto_detalle(request, pk):
    try:
        producto = Producto.objects.get(pk=pk, activo=True)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

# categorías
@api_view(['GET'])
def api_categorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)
