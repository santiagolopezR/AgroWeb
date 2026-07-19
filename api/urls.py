from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, FincaViewSet, LoteViewSet, CultivoCatalogoViewSet, CultivoEnLoteViewSet, ProductoViewSet, TipoActividadViewSet, ActividadViewSet, ActividadProductoViewSet, ActividadLoteViewSet, PrecioProductoViewSet, login_view

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('fincas', FincaViewSet)
router.register('lotes', LoteViewSet)
router.register('cultivos', CultivoCatalogoViewSet)
router.register('cultivos-en-lotes', CultivoEnLoteViewSet)
router.register('productos', ProductoViewSet)
router.register('tipos-actividad', TipoActividadViewSet)
router.register('actividades', ActividadViewSet)
router.register('actividad-productos', ActividadProductoViewSet)
router.register('actividad-lotes', ActividadLoteViewSet)
router.register('precio-productos', PrecioProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),
]