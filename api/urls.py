from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, FincaViewSet, LoteViewSet, CultivoCatalogoViewSet, CultivoEnLoteViewSet, ProductoViewSet, TipoActividadViewSet, ActividadViewSet, ActividadProductoViewSet

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

urlpatterns = [
    path('', include(router.urls)),
]