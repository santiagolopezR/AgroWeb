from rest_framework import serializers
from .models import Cliente, Finca, Lote, CultivoCatalogo, CultivoEnLote, Producto, TipoActividad, Actividad, ActividadProducto, ActividadLote, PrecioProducto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email']

class FincaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finca
        fields = ['id', 'cliente', 'nombre', 'ubicacion']

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ['id', 'finca', 'nombre', 'superficie']

class CultivoCatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivoCatalogo
        fields = ['id', 'nombre']

class CultivoEnLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivoEnLote
        fields = ['id', 'lote', 'cultivo', 'fecha_siembra']

class PrecioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioProducto
        fields = ['id', 'precio', 'fecha_vigencia']

class ProductoSerializer(serializers.ModelSerializer):
    precios = PrecioProductoSerializer(source='precios', many=True, read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'unidad', 'precio_actual', 'precios']

class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = ['id', 'nombre', 'requiere_productos']

class ActividadProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadProducto
        fields = ['id', 'actividad', 'producto', 'cantidad', 'costo_unitario', 'total']

class ActividadLoteSerializer(serializers.ModelSerializer):
    lote_nombre = serializers.CharField(source='lote.nombre', read_only=True)
    
    class Meta:
        model = ActividadLote
        fields = ['id', 'lote', 'lote_nombre', 'hectareas']

class ActividadSerializer(serializers.ModelSerializer):
    lotes_detalle = ActividadLoteSerializer(source='actividadlote_set', many=True, read_only=True)
    productos = ActividadProductoSerializer(many=True, source='actividadproducto_set', read_only=True)
    
    class Meta:
        model = Actividad
        fields = ['id', 'lotes_detalle', 'tipo', 'fecha', 'responsable', 'observaciones', 'productos']