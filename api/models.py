from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre

class Finca(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} ({self.cliente.nombre})"

class Lote(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    superficie = models.FloatField()
    coordenadas_poligono = JSONField(null=True, blank=True)
    latitud_centro = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitud_centro = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    area_calculada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.finca})"
    
class CultivoCatalogo(models.Model):
    nombre = models.CharField(max_length=100)
    ciclo_dias = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class CultivoEnLote(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(CultivoCatalogo, on_delete=models.CASCADE)
    fecha_siembra = models.DateField()
    
    def __str__(self):
        return f"{self.cultivo.nombre} en {self.lote.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.CharField(max_length=20)
    precio_actual = models.DecimalField(max_digits=18, decimal_places=2)
    bulto = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_vigencia = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_vigencia']
    
    def __str__(self):
        return f"{self.producto.nombre} - ${self.precio} ({self.fecha_vigencia})"

class Zafra(models.Model):
    ESTADO_CHOICES = [
        ('prep', 'Preparación'),
        ('siembra', 'Siembra'),
        ('crec', 'Crecimiento'),
        ('cosecha', 'Cosecha'),
        ('cerrada', 'Cerrada'),
    ]
    
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    numero_zafra = models.IntegerField()
    cultivo = models.ForeignKey(CultivoCatalogo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='prep')
    rendimiento_esperado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rendimiento_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ingresos_totales = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('lote', 'numero_zafra', 'user')
    
    def __str__(self):
        return f"Zafra {self.numero_zafra} - {self.cultivo.nombre}"
    
class TipoActividad(models.Model):
    nombre = models.CharField(max_length=50)
    requiere_productos = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    lotes = models.ManyToManyField(Lote, through='ActividadLote')
    tipo = models.ForeignKey(TipoActividad, on_delete=models.SET_NULL, null=True)
    zafra = models.ForeignKey(Zafra, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField()
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Costos adicionales
    cantidad_personas = models.IntegerField(null=True, blank=True)
    horas_trabajo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_jornal = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_mano_obra = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    tipo_maquina = models.CharField(max_length=255, null=True, blank=True)
    horas_maquina = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_hora_maquina = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_maquina = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    tipo_combustible = models.CharField(max_length=100, null=True, blank=True)
    cantidad_combustible = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    precio_combustible = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_combustible = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    costos_adicionales = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    costo_total = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo.nombre} ({self.fecha})"

class ActividadLote(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    hectareas = models.FloatField(default=0)
    
    class Meta:
        unique_together = ('actividad', 'lote')
    
    def __str__(self):
        return f"{self.actividad} - {self.lote}"

class ActividadProducto(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} en {self.actividad}"

class ActividadSiembra(models.Model):
    actividad = models.OneToOneField(Actividad, on_delete=models.CASCADE)
    semilla = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='siembras_semilla')
    cantidad_kg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    precio = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    fertilizante = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='siembras_fertilizante')
    cantidad_fertilizante_kg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    precio_fertilizante = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    distancia_surco_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distancia_plantas_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profundidad_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Siembra - Actividad {self.actividad.id}"

class ActividadCosecha(models.Model):
    actividad = models.OneToOneField(Actividad, on_delete=models.CASCADE)
    rendimiento_kg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    precio_venta_kg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ingresos_totales = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    transporte_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_transporte = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_gasto = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cosecha - Actividad {self.actividad.id}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    nit = models.CharField(max_length=50, null=True, blank=True)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class TipoCosto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class FincaGasto(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    zafra = models.ForeignKey(Zafra, on_delete=models.CASCADE, null=True, blank=True)
    factura_numero = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19)
    observaciones = models.TextField(null=True, blank=True)
    total_bruto = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Gasto {self.factura_numero}"

class FincaGastoItem(models.Model):
    gasto = models.ForeignKey(FincaGasto, on_delete=models.CASCADE, related_name='items')
    tipo_costo = models.ForeignKey(TipoCosto, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.CharField(max_length=500)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    unidad = models.CharField(max_length=50, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Item - {self.descripcion}"