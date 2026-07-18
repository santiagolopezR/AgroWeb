from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Cliente, Finca, Lote, CultivoCatalogo, CultivoEnLote, Producto, TipoActividad, Actividad, ActividadProducto
from .serializers import ClienteSerializer, FincaSerializer, LoteSerializer, CultivoCatalogoSerializer, CultivoEnLoteSerializer, ProductoSerializer, TipoActividadSerializer, ActividadSerializer, ActividadProductoSerializer

class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]

class FincaViewSet(ModelViewSet):
    queryset = Finca.objects.all()
    serializer_class = FincaSerializer
    permission_classes = [AllowAny]

class LoteViewSet(ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [AllowAny]

class CultivoCatalogoViewSet(ModelViewSet):
    queryset = CultivoCatalogo.objects.all()
    serializer_class = CultivoCatalogoSerializer
    permission_classes = [AllowAny]

class CultivoEnLoteViewSet(ModelViewSet):
    queryset = CultivoEnLote.objects.all()
    serializer_class = CultivoEnLoteSerializer
    permission_classes = [AllowAny]

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]

class TipoActividadViewSet(ModelViewSet):
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
    permission_classes = [AllowAny]

class ActividadViewSet(ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [AllowAny]

class ActividadProductoViewSet(ModelViewSet):
    queryset = ActividadProducto.objects.all()
    serializer_class = ActividadProductoSerializer
    permission_classes = [AllowAny]


from django.http import JsonResponse

def prueba(request):
    return JsonResponse({"mensaje": "Django funciona en Railway"})