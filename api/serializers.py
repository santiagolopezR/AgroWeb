from rest_framework import serializers
from .models import (
    Cliente, Finca, Lote, CultivoCatalogo, CultivoEnLote, Producto, TipoActividad, 
    Actividad, ActividadProducto, ActividadLote, PrecioProducto, Zafra, ActividadSiembra, 
    ActividadCosecha, Proveedor, TipoCosto, FincaGasto, FincaGastoItem, Categoria,
    
)
from .models import (PrestamoTrabajador, AbonoPrestamo, CostoFijo, CostoAdicional)
# ==========================================
# FASE 1: DATOS MAESTROS
# ==========================================

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'user_id']
        read_only_fields = ['id', 'user_id']


class FincaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finca
        fields = ['id', 'cliente', 'nombre', 'ubicacion', 'user_id']
        read_only_fields = ['id', 'user_id']


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ['id', 'finca', 'nombre', 'superficie', 'user_id', 'coordenadas_poligono', 
                  'latitud_centro', 'longitud_centro', 'area_hectareas']
        read_only_fields = ['id', 'user_id']


class CultivoCatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivoCatalogo
        fields = ['id', 'nombre']


class CultivoEnLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultivoEnLote
        fields = ['id', 'lote', 'cultivo', 'fecha_siembra']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'unidad', 'precio_actual', 'user_id']
        read_only_fields = ['id', 'user_id']


class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = ['id', 'nombre', 'requiere_productos']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'user_id']
        read_only_fields = ['id', 'user_id']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'contacto', 'email', 'nit', 'activo', 'user_id']
        read_only_fields = ['id', 'user_id']


class TipoCostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCosto
        fields = ['id', 'nombre']


# ==========================================
# FASE 2: ACTIVIDADES Y PRODUCTOS
# ==========================================

class PrecioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioProducto
        fields = ['id', 'producto', 'precio', 'fecha_vigencia']


class ActividadProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadProducto
        fields = ['id', 'actividad', 'producto', 'cantidad', 'costo_unitario', 'total', 'dosis_por_hectarea']


class ActividadLoteSerializer(serializers.ModelSerializer):
    lote_nombre = serializers.CharField(source='lote.nombre', read_only=True)
    
    class Meta:
        model = ActividadLote
        fields = ['id', 'actividad', 'lote', 'lote_nombre', 'hectareas', 'user_id']
        read_only_fields = ['id', 'user_id']


class ActividadSerializer(serializers.ModelSerializer):
    lotes_detalle = ActividadLoteSerializer(source='actividadlote_set', many=True, read_only=True)
    productos = ActividadProductoSerializer(many=True, source='actividadproducto_set', read_only=True)
    
    class Meta:
        model = Actividad
        fields = ['id', 'finca', 'tipo', 'fecha', 'responsable', 'observaciones', 'productos', 'lotes_detalle', 'jornales_cantidad', 'costo_total', 'detalle_costos', 'user_id']
        read_only_fields = ['id', 'user_id']


# ==========================================
# FASE 3: ZAFRAS Y COSECHAS
# ==========================================

class ZafraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zafra
        fields = ['id', 'lote', 'numero_zafra', 'cultivo', 'fecha_inicio', 'fecha_fin', 'estado', 'rendimiento', 'precio_venta', 'ingresos_totales', 'user_id']
        read_only_fields = ['id', 'user_id']


class ActividadSiembraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadSiembra
        fields = '__all__'
        read_only_fields = ['id']


class ActividadCosechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadCosecha
        fields = '__all__'
        read_only_fields = ['id']


# ==========================================
# FASE 4: GASTOS Y COSTOS
# ==========================================

class FincaGastoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FincaGastoItem
        fields = ['id', 'gasto', 'tipo_costo', 'descripcion', 'cantidad', 'unidad', 'precio_unitario', 'total']
        read_only_fields = ['id']


class FincaGastoSerializer(serializers.ModelSerializer):
    items = FincaGastoItemSerializer(source='fincagastoitem_set', many=True, read_only=True)
    
    class Meta:
        model = FincaGasto
        fields = ['id', 'finca', 'factura', 'proveedor', 'fecha', 'iva_porcentaje', 'total_neto', 'total_iva', 'total_general', 'items', 'user_id']
        read_only_fields = ['id', 'user_id']


class CostoFijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostoFijo
        fields = ['id', 'nombre', 'valor_unitario', 'unidad', 'activo', 'user_id']
        read_only_fields = ['id', 'user_id']


class CostoAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostoAdicional
        fields = ['id', 'actividad', 'costo_fijo', 'cantidad', 'user_id']
        read_only_fields = ['id', 'user_id']


# ==========================================
# FASE 5: PRÉSTAMOS
# ==========================================

class PrestamoTrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoTrabajador
        fields = ['id', 'nombre_trabajador', 'quien_otorga', 'monto_inicial', 'fecha_otorgamiento', 'activo', 'user_id']
        read_only_fields = ['id', 'user_id']


class AbonoPrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbonoPrestamo
        fields = ['id', 'prestamo', 'monto', 'fecha_abono', 'quien_descuenta', 'user_id']
        read_only_fields = ['id', 'user_id']
