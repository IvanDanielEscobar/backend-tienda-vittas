from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Usuario

class RegistroUsuarioForm(UserCreationForm):
    # Agregamos explícitamente los campos adicionales al formulario de creación
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    direccion = forms.CharField(max_length=255, required=False, label="Dirección de Envío")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'telefono', 'direccion')


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'categoria', 'descripcion', 'talles', 'imagen', 'es_talle_unico']
        widgets = {
            'talles': forms.CheckboxSelectMultiple,
        }