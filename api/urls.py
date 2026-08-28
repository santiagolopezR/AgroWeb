from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, FincaViewSet, LoteViewSet, CultivoCatalogoViewSet, CultivoEnLoteViewSet, 
    ProductoViewSet, TipoActividadViewSet, ActividadViewSet, ActividadProductoViewSet, 
    ActividadLoteViewSet, PrecioProductoViewSet, login_view, ZafraViewSet, ActividadSiembraViewSet, 
    ActividadCosechaViewSet, ProveedorViewSet, TipoCostoViewSet, CategoriaViewSet, FincaGastoViewSet, 
    FincaGastoItemViewSet, CostoFijoViewSet, CostoAdicionalViewSet, PrestamoTrabajadorViewSet, AbonoPrestamoViewSet
)

router = DefaultRouter()

# Fase 1
router.register('clientes', ClienteViewSet, basename='cliente')
router.register('fincas', FincaViewSet, basename='finca')
router.register('lotes', LoteViewSet, basename='lote')
router.register('cultivos', CultivoCatalogoViewSet, basename='cultivo')
router.register('cultivos-en-lotes', CultivoEnLoteViewSet, basename='cultivo-en-lote')
router.register('productos', ProductoViewSet, basename='producto')
router.register('tipos-actividad', TipoActividadViewSet, basename='tipo-actividad')
router.register('actividades', ActividadViewSet, basename='actividad')
router.register('actividad-productos', ActividadProductoViewSet, basename='actividad-producto')
router.register('actividad-lotes', ActividadLoteViewSet, basename='actividad-lote')
router.register('precio-productos', PrecioProductoViewSet, basename='precio-producto')

# Fase 3
router.register('zafras', ZafraViewSet, basename='zafra')
router.register('actividad-siembra', ActividadSiembraViewSet, basename='actividad-siembra')
router.register('actividad-cosecha', ActividadCosechaViewSet, basename='actividad-cosecha')

# Datos Maestros
router.register('proveedores', ProveedorViewSet, basename='proveedor')
router.register('tipos-costo', TipoCostoViewSet, basename='tipo-costo')
router.register('categorias', CategoriaViewSet, basename='categoria')

# Fase 4
router.register('finca-gastos', FincaGastoViewSet, basename='finca-gasto')
router.register('finca-gasto-items', FincaGastoItemViewSet, basename='finca-gasto-item')
router.register('costos-fijos', CostoFijoViewSet, basename='costo-fijo')
router.register('costos-adicionales', CostoAdicionalViewSet, basename='costo-adicional')

# Fase 5
router.register('prestamos', PrestamoTrabajadorViewSet, basename='prestamo')
router.register('abonos', AbonoPrestamoViewSet, basename='abono')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),
]