from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # pag principales
    path('', views.CatalogoView.as_view(), name='catalogo'),
    path('producto/<int:pk>/', views.ProductoDetalleView.as_view(), name='detalle_producto'),
    #autenticaciones
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='tienda/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # API
    path('api/productos/', views.api_productos, name='api_productos'),
    path('api/producto/<int:pk>/', views.api_producto_detalle, name='api_producto_detalle'),
    path('api/categorias/', views.api_categorias, name='api_categorias'),
    #crud productos
    path('panel/productos/', views.PanelProductoListView.as_view(), name='panel_productos'),
    path('panel/producto/nuevo', views.CrearProductoView.as_view(), name='crear_producto'),
    path('panel/producto/<int:pk>/editar', views.EditarProductoView.as_view(), name='editar_producto'),
    path('panel/producto/<int:pk>/borrar', views.BorrarProductoView.as_view(), name='borrar_producto'),
    # crud categorias
    path('panel/categorias/', views.CategoriaListView.as_view(), name='crud_categorias'),
    path('panel/categorias/nuevo/', views.CategoriaCreateView.as_view(), name='crear_categoria'),
    path('panel/categorias/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('panel/categorias/borrar/<int:pk>/', views.CategoriaDeleteView.as_view(), name='borrar_categoria'),
    # crud talles
    path('panel/talles/', views.TalleListView.as_view(), name='crud_talles'),
    path('panel/talles/nuevo/', views.TalleCreateView.as_view(), name='crear_talle'),
    path('panel/talles/editar/<int:pk>/', views.TalleUpdateView.as_view(), name='editar_talle'),
    path('panel/talles/borrar/<int:pk>/', views.TalleDeleteView.as_view(), name='borrar_talle'),
]