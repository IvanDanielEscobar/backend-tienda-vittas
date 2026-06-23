from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Producto, Usuario
Usuario = get_user_model()

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
            'talles': forms.CheckboxSelectMultiple(attrs={
                'class': 'rounded text-indigo-600 focus:ring-indigo-500 border-gray-300'
            }),
            'es_talle_unico': forms.CheckboxInput(attrs={
                'class': 'rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Describí las características de la prenda...'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['talles', 'es_talle_unico', 'imagen']:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm placeholder-gray-400 transition-all shadow-sm'
                })


class EmpleadoForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm'}),
        label="Contraseña")
    
    # para elegir el puesto de trabajo
    PUESTOS_CHOICES = [
        ('vendedores', 'Vendedor (Gestión de Stock y Catálogo)'),
        ('tesoreros', 'Tesorero (Gestión de Caja y Pedidos)'),
        ('cajeros', 'Cajero (Gestión de Caja y Pedidos)'),
        ('administradores', 'Administrador (Gestión de Usuarios y Roles)'),
    ]
    puestos = forms.MultipleChoiceField(
        choices=PUESTOS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'rounded text-indigo-600 focus:ring-indigo-500 h-4 w-4 border-gray-300'}),
        label="Puesto / Rol Asignado"
        )

    class Meta:
        model = Usuario
        fields = ['username',  'first_name', 'last_name', 'email','telefono', 'direccion', 'password']
        labels = {
                'username': 'Nombre de Usuario (Legajo/CUIL)',
                'first_name': 'Nombre',
                'last_name': 'Apellido',
                'email': 'Correo Electrónico',
                'telefono': 'Teléfono de Contacto',
                'direccion': 'Dirección Particular',
            }
        #tailwind para los campos del formulario
        widgets = {
            f: forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm'})
            for f in ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion']
        }
        
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        usuario.is_staff = True
        if commit:
            usuario.save()
            usuario.groups.clear()
            roles_seleccionados = self.cleaned_data['puestos']
            for rol in roles_seleccionados:
                if rol == 'vendedores':
                    grupo, _ = Group.objects.get_or_create(name='Vendedores')
                elif rol == 'tesoreros':
                    grupo, _ = Group.objects.get_or_create(name='Tesoreros')
                elif rol == 'cajeros':
                    grupo, _ = Group.objects.get_or_create(name='Cajeros')
                elif rol == 'administradores':
                    grupo, _ = Group.objects.get_or_create(name='Administradores')
                
                usuario.groups.add(grupo)
        return usuario