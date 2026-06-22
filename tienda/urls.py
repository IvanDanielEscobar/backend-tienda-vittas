from django.urls import path
from . import views

urlpatterns = [
    path('', views.CatalogoView.as_view(), name='catalogo'),
    path('api/productos/', views.api_productos, name='api_productos'),
    path('api/producto/<int:pk>/', views.api_producto_detalle, name='api_producto_detalle'),
    path('api/categorias/', views.api_categorias, name='api_categorias'),

    path('producto/<int:pk>/', views.ProductoDetalleView.as_view(), name='detalle_producto'),
    path('registro/', views.registro_usuario, name='registro'),
]