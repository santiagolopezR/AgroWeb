from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre

class Finca(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre} ({self.cliente.nombre})"

class Lote(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # ← AGREGAR
    nombre = models.CharField(max_length=100)
    superficie = models.FloatField()
    
    def __str__(self):
        return f"{self.nombre} ({self.finca})"
    
class CultivoCatalogo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class CultivoEnLote(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    cultivo = models.ForeignKey(CultivoCatalogo, on_delete=models.CASCADE)
    fecha_siembra = models.DateField()
    
    def __str__(self):
        return f"{self.cultivo.nombre} en {self.lote.nombre}"

class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # ← AGREGAR
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    unidad = models.CharField(max_length=20)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
class PrecioProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vigencia = models.DateField()
    
    class Meta:
        ordering = ['-fecha_vigencia']
    
    def __str__(self):
        return f"{self.producto.nombre} - ${self.precio} ({self.fecha_vigencia})"
    
class TipoActividad(models.Model):
    nombre = models.CharField(max_length=50)
    requiere_productos = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    lotes = models.ManyToManyField(Lote, through='ActividadLote')
    tipo = models.ForeignKey(TipoActividad, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    
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
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} en {self.actividad}"