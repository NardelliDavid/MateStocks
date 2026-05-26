from django.db import models

# Create your models here.
class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    stock_minimo = models.PositiveIntegerField()
    ultima_fecha_actualizacion_precio = models.DateTimeField(auto_now_add=True)