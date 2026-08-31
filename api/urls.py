from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    FincaViewSet,
    LoteViewSet,
    ProductoViewSet,
    CultivoCatalogoViewSet,
    CultivoEnLoteViewSet,
    TipoActividadViewSet,
    CategoriaViewSet,
    ProveedorViewSet,
    TipoCostoViewSet,
    ActividadViewSet,
    ActividadProductoViewSet,
    ActividadLoteViewSet,
    PrecioProductoViewSet,
    ZafraViewSet,
    ActividadSiembraViewSet,
    ActividadCosechaViewSet,
    FincaGastoViewSet,
    FincaGastoItemViewSet,
    CostoFijoViewSet,
    CostoAdicionalViewSet,
    PrestamoTrabajadorViewSet,
    AbonoPrestamoViewSet,
)

router = DefaultRouter()

router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'fincas', FincaViewSet, basename='finca')
router.register(r'lotes', LoteViewSet, basename='lote')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'cultivos-catalogo', CultivoCatalogoViewSet, basename='cultivo-catalogo')
router.register(r'cultivos-en-lote', CultivoEnLoteViewSet, basename='cultivo-en-lote')
router.register(r'tipos-actividad', TipoActividadViewSet, basename='tipo-actividad')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'tipos-costo', TipoCostoViewSet, basename='tipo-costo')
router.register(r'actividades', ActividadViewSet, basename='actividad')
router.register(r'actividades-productos', ActividadProductoViewSet, basename='actividad-producto')
router.register(r'actividades-lotes', ActividadLoteViewSet, basename='actividad-lote')
router.register(r'precios-productos', PrecioProductoViewSet, basename='precio-producto')
router.register(r'zafras', ZafraViewSet, basename='zafra')
router.register(r'actividades-siembra', ActividadSiembraViewSet, basename='actividad-siembra')
router.register(r'actividades-cosecha', ActividadCosechaViewSet, basename='actividad-cosecha')
router.register(r'gastos', FincaGastoViewSet, basename='gasto')
router.register(r'gastos-items', FincaGastoItemViewSet, basename='gasto-item')
router.register(r'costos-fijos', CostoFijoViewSet, basename='costo-fijo')
router.register(r'costos-adicionales', CostoAdicionalViewSet, basename='costo-adicional')
router.register(r'prestamos', PrestamoTrabajadorViewSet, basename='prestamo')
router.register(r'abonos', AbonoPrestamoViewSet, basename='abono')

urlpatterns = [
    path('', include(router.urls)),
]