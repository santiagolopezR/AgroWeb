from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, FincaViewSet, LoteViewSet, CultivoCatalogoViewSet, CultivoEnLoteViewSet, ProductoViewSet, TipoActividadViewSet, ActividadViewSet, ActividadProductoViewSet, ActividadLoteViewSet, PrecioProductoViewSet, login_view
from .views import ZafraViewSet, ActividadSiembraViewSet, ActividadCosechaViewSet, ProveedorViewSet, TipoCostoViewSet, CategoriaViewSet, FincaGastoViewSet, FincaGastoItemViewSet

router = DefaultRouter()
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
router = DefaultRouter()
router.register(r'zafras', ZafraViewSet)
router.register(r'actividad-siembra', ActividadSiembraViewSet)
router.register(r'actividad-cosecha', ActividadCosechaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'tipos-costo', TipoCostoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'finca-gastos', FincaGastoViewSet)
router.register(r'finca-gasto-items', FincaGastoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),
]