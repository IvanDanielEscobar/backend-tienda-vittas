from rest_framework import serializers
from .models import Producto, Categoria, VarianteProducto, Talle

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class TalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talle
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='categoria.nombre')
    imagenes = serializers.SerializerMethodField()
    talles = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'categoria', 'descripcion', 'imagenes', 'talles', 'es_talle_unico', 'stock']

    def get_imagenes(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request is not None:
                return [request.build_absolute_uri(obj.imagen.url)]
            return [obj.imagen.url]
        return []

    def get_talles(self, obj):
        return [variante.talle.nombre for variante in obj.variantes.all()]

    def get_stock(self, obj):
        return {variante.talle.nombre: variante.stock for variante in obj.variantes.all()}