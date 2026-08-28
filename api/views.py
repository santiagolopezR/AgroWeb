from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from .models import (
    Cliente, Finca, Lote, Producto, CultivoCatalogo, CultivoEnLote,
    TipoActividad, Actividad, ActividadLote, ActividadProducto,
    Categoria, PrecioProducto, Zafra, ActividadSiembra, ActividadCosecha,
    Proveedor, TipoCosto, FincaGasto, FincaGastoItem, PrestamoTrabajador,
    AbonoPrestamo, CostoFijo, CostoAdicional
)

from .serializers import (
    ClienteSerializer, FincaSerializer, LoteSerializer,
    CultivoCatalogoSerializer, CultivoEnLoteSerializer, ProductoSerializer,
    TipoActividadSerializer, ActividadSerializer, ActividadProductoSerializer,
    ActividadLoteSerializer, CategoriaSerializer, PrecioProductoSerializer,
    ZafraSerializer, ActividadSiembraSerializer, ActividadCosechaSerializer,
    ProveedorSerializer, TipoCostoSerializer, FincaGastoSerializer,
    FincaGastoItemSerializer, PrestamoTrabajadorSerializer, AbonoPrestamoSerializer,
    CostoFijoSerializer, CostoAdicionalSerializer
)

# ==========================================
# PERMISSION CLASSES
# ==========================================

class IsOwner(permissions.BasePermission):
    """Permite acceso solo al propietario (user_id)"""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.id
        return False

# ==========================================
# FASE 1: DATOS MAESTROS
# ==========================================

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Cliente.objects.none()
        return Cliente.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este cliente")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este cliente")
        instance.delete()


class FincaViewSet(viewsets.ModelViewSet):
    serializer_class = FincaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Finca.objects.none()
        return Finca.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta finca")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta finca")
        instance.delete()


class LoteViewSet(viewsets.ModelViewSet):
    serializer_class = LoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Lote.objects.none()
        return Lote.objects.filter(finca__user_id=self.request.user.id)

    def perform_create(self, serializer):
        finca = serializer.validated_data.get('finca')
        if finca.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear lotes en esta finca")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.finca.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este lote")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.finca.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este lote")
        instance.delete()


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Producto.objects.none()
        return Producto.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este producto")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este producto")
        instance.delete()


class CultivoCatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CultivoCatalogo.objects.all()
    serializer_class = CultivoCatalogoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CultivoEnLoteViewSet(viewsets.ModelViewSet):
    serializer_class = CultivoEnLoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return CultivoEnLote.objects.none()
        return CultivoEnLote.objects.filter(lote__finca__user_id=self.request.user.id)

    def perform_create(self, serializer):
        lote = serializer.validated_data.get('lote')
        if lote.finca.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear cultivos en este lote")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.lote.finca.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este cultivo")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.lote.finca.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este cultivo")
        instance.delete()


class TipoActividadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Categoria.objects.none()
        return Categoria.objects.filter(
            Q(user_id__isnull=True) | Q(user_id=self.request.user.id)
        )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id and obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta categoría")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta categoría")
        instance.delete()


class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Proveedor.objects.none()
        return Proveedor.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este proveedor")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este proveedor")
        instance.delete()


class TipoCostoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoCosto.objects.all()
    serializer_class = TipoCostoSerializer
    permission_classes = [permissions.IsAuthenticated]


# ==========================================
# FASE 2: ACTIVIDADES Y PRODUCTOS
# ==========================================

class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Actividad.objects.none()
        return Actividad.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        finca = serializer.validated_data.get('finca')
        if finca.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear actividades en esta finca")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta actividad")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta actividad")
        instance.delete()


class ActividadProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadProductoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return ActividadProducto.objects.none()
        return ActividadProducto.objects.filter(actividad__user_id=self.request.user.id)

    def perform_create(self, serializer):
        actividad = serializer.validated_data.get('actividad')
        if actividad.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar productos a esta actividad")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este producto en actividad")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este producto en actividad")
        instance.delete()


class ActividadLoteViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadLoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return ActividadLote.objects.none()
        return ActividadLote.objects.filter(actividad__user_id=self.request.user.id)

    def perform_create(self, serializer):
        actividad = serializer.validated_data.get('actividad')
        if actividad.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar lotes a esta actividad")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este lote en actividad")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este lote en actividad")
        instance.delete()


class PrecioProductoViewSet(viewsets.ModelViewSet):
    serializer_class = PrecioProductoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return PrecioProducto.objects.none()
        return PrecioProducto.objects.filter(producto__user_id=self.request.user.id)

    def perform_create(self, serializer):
        producto = serializer.validated_data.get('producto')
        if producto.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar precios a este producto")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.producto.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este precio")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.producto.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este precio")
        instance.delete()


# ==========================================
# FASE 3: ZAFRAS Y COSECHAS
# ==========================================

class ZafraViewSet(viewsets.ModelViewSet):
    serializer_class = ZafraSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Zafra.objects.none()
        return Zafra.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta zafra")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta zafra")
        instance.delete()


class ActividadSiembraViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSiembraSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return ActividadSiembra.objects.none()
        return ActividadSiembra.objects.filter(actividad__user_id=self.request.user.id)

    def perform_create(self, serializer):
        actividad = serializer.validated_data.get('actividad')
        if actividad.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear siembras en esta actividad")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta siembra")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta siembra")
        instance.delete()


class ActividadCosechaViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadCosechaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return ActividadCosecha.objects.none()
        return ActividadCosecha.objects.filter(actividad__user_id=self.request.user.id)

    def perform_create(self, serializer):
        actividad = serializer.validated_data.get('actividad')
        if actividad.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear cosechas en esta actividad")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar esta cosecha")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar esta cosecha")
        instance.delete()


# ==========================================
# FASE 4: GASTOS Y COSTOS
# ==========================================

class FincaGastoViewSet(viewsets.ModelViewSet):
    serializer_class = FincaGastoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return FincaGasto.objects.none()
        return FincaGasto.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        finca = serializer.validated_data.get('finca')
        if finca.user_id != self.request.user.id:
            raise PermissionDenied("No puedes crear gastos en esta finca")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este gasto")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este gasto")
        instance.delete()


class FincaGastoItemViewSet(viewsets.ModelViewSet):
    serializer_class = FincaGastoItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return FincaGastoItem.objects.none()
        return FincaGastoItem.objects.filter(gasto__user_id=self.request.user.id)

    def perform_create(self, serializer):
        gasto = serializer.validated_data.get('gasto')
        if gasto.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar items a este gasto")
        serializer.save()

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.gasto.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este item")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.gasto.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este item")
        instance.delete()


class CostoFijoViewSet(viewsets.ModelViewSet):
    serializer_class = CostoFijoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return CostoFijo.objects.none()
        return CostoFijo.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este costo fijo")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este costo fijo")
        instance.delete()


class CostoAdicionalViewSet(viewsets.ModelViewSet):
    serializer_class = CostoAdicionalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return CostoAdicional.objects.none()
        return CostoAdicional.objects.filter(actividad__user_id=self.request.user.id)

    def perform_create(self, serializer):
        actividad = serializer.validated_data.get('actividad')
        if actividad.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar costos a esta actividad")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este costo")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.actividad.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este costo")
        instance.delete()


# ==========================================
# FASE 5: PRÉSTAMOS
# ==========================================

class PrestamoTrabajadorViewSet(viewsets.ModelViewSet):
    serializer_class = PrestamoTrabajadorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return PrestamoTrabajador.objects.none()
        return PrestamoTrabajador.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este préstamo")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este préstamo")
        instance.delete()


class AbonoPrestamoViewSet(viewsets.ModelViewSet):
    serializer_class = AbonoPrestamoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return AbonoPrestamo.objects.none()
        return AbonoPrestamo.objects.filter(prestamo__user_id=self.request.user.id)

    def perform_create(self, serializer):
        prestamo = serializer.validated_data.get('prestamo')
        if prestamo.user_id != self.request.user.id:
            raise PermissionDenied("No puedes agregar abonos a este préstamo")
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.prestamo.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para editar este abono")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.prestamo.user_id != self.request.user.id:
            raise PermissionDenied("No tienes permiso para eliminar este abono")
        instance.delete()