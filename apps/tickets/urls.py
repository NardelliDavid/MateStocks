from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tickets/agregar_producto_ticket", views.agregar_producto_ticket, name="agregar_producto_ticket"),
    path("tickets/buscar_producto_ticket", views.buscar_producto_ticket, name="buscar_producto_ticket"),
    path("tickets/recargarTablaIndex", views.recargarTablaIndex, name='recargarTablaIndex'),
    path("tickets/quitarProductoDelTicket", views.quitarProductoDelTicket, name='quitarProductoDelTicket'),
    path("tickets/vaciarTicket", views.vaciarTicket, name="vaciarTicket"),
    path("tickets/ticketCreado", views.ticketCreado, name='ticketCreado'),
    path("tickets/verTicket/<int:id_ticket>", views.verTicket, name="verTicket"),
    path("tickets/historial_tickets", views.historial_tickets, name="historial_tickets")
]