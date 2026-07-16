from django.db import models

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
    nombre = models.CharField(max_length=100)
    superficie = models.FloatField()
    
    def __str__(self):
        return self.nombre

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
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    unidad = models.CharField(max_length=20)
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre

class TipoActividad(models.Model):
    nombre = models.CharField(max_length=50)
    requiere_productos = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    cultivo_en_lote = models.ForeignKey(CultivoEnLote, on_delete=models.CASCADE, null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoActividad, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.tipo.nombre} en {self.lote.nombre} ({self.fecha})"

class ActividadProducto(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} en {self.actividad}"