from django.db import models

# Create your models here.
class Tickets(models.Model):
    fecha_y_hora = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=30)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Detalle_ticket(models.Model):
    id_ticket = models.IntegerField()
    codigo_barras = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)