from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Producto, Categoria, Talle, Pedido, DetallePedido
from .forms import RegistroUsuarioForm
from .serializers import ProductoSerializer, CategoriaSerializer
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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

# --- CRUD DE CATEGORÍAS ---

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'tienda/crud_categorias.html'
    context_object_name = 'categorias'

class CategoriaCreateView(PermissionRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'tienda/form_categoria.html'
    success_url = reverse_lazy('crud_categorias')
    permission_required = 'tienda.add_categoria' # Permiso nativo de Django

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


# --- CRUD DE TALLES ---

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