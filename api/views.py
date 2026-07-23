from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Cliente, Finca, Lote, CultivoCatalogo, CultivoEnLote, Producto, TipoActividad, Actividad, ActividadProducto, ActividadLote, PrecioProducto
from .serializers import ClienteSerializer, FincaSerializer, LoteSerializer, CultivoCatalogoSerializer, CultivoEnLoteSerializer, ProductoSerializer, TipoActividadSerializer, ActividadSerializer, ActividadProductoSerializer, ActividadLoteSerializer, PrecioProductoSerializer

# Login endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user.username})
    else:
        return Response({'error': 'Credenciales inválidas'}, status=400)

# ViewSets
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Lote.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CultivoCatalogoViewSet(ModelViewSet):
    queryset = CultivoCatalogo.objects.all()
    serializer_class = CultivoCatalogoSerializer
    permission_classes = [AllowAny]

class CultivoEnLoteViewSet(ModelViewSet):
    queryset = CultivoEnLote.objects.all()
    serializer_class = CultivoEnLoteSerializer
    permission_classes = [AllowAny]

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()  # ← AGREGAR
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Producto.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

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

class ActividadLoteViewSet(ModelViewSet):
    queryset = ActividadLote.objects.all()
    serializer_class = ActividadLoteSerializer
    permission_classes = [IsAuthenticated]

class PrecioProductoViewSet(ModelViewSet):
    queryset = PrecioProducto.objects.all()
    serializer_class = PrecioProductoSerializer
    permission_classes = [IsAuthenticated]