from django.urls import path
from . import views

urlpatterns = [
    path("crud_productos", views.crud_productos, name="crud_productos"),
    path("modificar_precio_stock", views.modificar_precio_stock, name="modificar_precio_stock"),
    path("agregar_producto", views.agregar_producto, name="agregar_producto"),
    path("partials/recargarTablaHTMX", views.recargarTablaHTMX, name="recargarTablaHTMX"),
    path("partials/recargarTablaHTMX_MPS", views.recargarTablaHTMX_MPS, name="recargarTablaHTMX_MPS"),
    path("eliminar_producto", views.eliminar_producto, name="eliminar_producto"),
    path("editar_producto", views.editar_producto, name="editar_producto"),
    path("modificar_precio_stock_CRUD", views.modificar_precio_stock_CRUD, name="modificar_precio_stock_CRUD")
]