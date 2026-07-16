from django.contrib import admin
from .models import Cliente, Finca, Lote, CultivoCatalogo, CultivoEnLote, Producto, TipoActividad, Actividad, ActividadProducto

admin.site.register(Cliente)
admin.site.register(Finca)
admin.site.register(Lote)
admin.site.register(CultivoCatalogo)
admin.site.register(CultivoEnLote)
admin.site.register(Producto)
admin.site.register(TipoActividad)
admin.site.register(Actividad)
admin.site.register(ActividadProducto)