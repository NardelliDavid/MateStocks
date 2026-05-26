from django.shortcuts import render, redirect
from apps.productos.models import Producto
from django.http import HttpResponse
from .validators import *
from django.utils import timezone

# Create your views here.
def crud_productos(request):
    productos = Producto.objects.all()

    return render(request, "productos/crud_productos.html", {
        "productos": productos
    })

def modificar_precio_stock(request):
    productos = Producto.objects.all().order_by('-ultima_fecha_actualizacion_precio')

    return render(request, "productos/modificar_precio_stock.html", {
        "productos": productos
    })

# Vistas de crud_productos
# ---------------------------------------

def recargarTablaHTMX(request):
    productos = Producto.objects.all()
    return render(request, "productos/partials/tbody_crud_productos.html", {
        "productos": productos
    })

# FUNCION QUE AGREGA EL PRODUCTO
def agregar_producto(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'): # Verifica que la peticion sea HX-Request
            try: # Obtiene los datos del formulario
                codigo_barras = request.POST["codigo_barras"]
                descripcion = request.POST["descripcion"]
                precio = request.POST["precio"]
                stock = request.POST["stock"]
                stock_minimo = request.POST["stock_minimo"]
                
                # VALIDACIONES DE LOS DATOS

                validez, resultado = validar_datos_productos_CREATE(codigo_barras, descripcion, precio, stock, stock_minimo)
                if not validez:
                    return HttpResponse(resultado)

                # VERIFICA QUE SI EXISTE LA MISMA DESCRIPCION O CODIGO DE BARRAS
                existe_cod_barras = False
                if resultado["codigo_barras"] is not None:
                    existe_cod_barras = Producto.objects.filter(codigo_barras = resultado["codigo_barras"]).exists()
                existe_descripcion = Producto.objects.filter(descripcion = resultado["descripcion"]).exists()

                # SI UNO DE LOS 2 ES VERDADERO ENVIA UN MENSAJE DE ERROR
                if existe_cod_barras or existe_descripcion:
                    return HttpResponse('<p class="text-red-600">Este producto ya existe en la base de datos!</p>')
                else:
                    # AGREGA EL PRODUCTO A LA BBDD
                    Producto.objects.create(
                        codigo_barras = resultado["codigo_barras"],
                        descripcion = resultado["descripcion"],
                        precio = resultado["precio"],
                        stock = resultado["stock"],
                        stock_minimo = resultado["stock_minimo"]
                    )
                    # MENSAJE DE EXITO AL AGREGAR PRODUCTO
                    response = HttpResponse('<p class="text-green-600">'+str(resultado["descripcion"])+' agregado/s con exito!</p>')
                    response["HX-Trigger"] = "recargarTabla" # Llama al evento "recargarTabla" cuando la respuesta llega a la plantilla
                    return response
            except Exception as error:
                return HttpResponse('<p class="text-red-600">Error al agregar producto: '+str(error)+'</p>')
    return redirect('crud_productos')

def eliminar_producto(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):
            try: # Obtiene el id enviado desde la plantilla
                id_producto = request.POST.get("id_producto") 
                consulta = Producto.objects.filter(id=id_producto)
                if consulta.exists(): # Si encuentra objetos con el mismo ID los borra
                    consulta.delete()
                    response = HttpResponse('<p class="text-green-600"> Producto eliminado correctamente!</p>')
                    response["HX-Trigger"] = "recargarTabla" # Activa el evento recargar tabla cuando es enviada la respuesta
                else:
                    response = HttpResponse('<p class="text-red-600">Error al intentar eliminar un producto: No se a encontrado en la base de datos.</p>')
                return response
            except Exception as error:
                return HttpResponse("ERROR AL ELIMINAR PRODUCTO: "+str(error))
    return redirect('crud_productos')
            
def editar_producto(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):
            try:
                id_producto = request.POST.get("id_producto")
                
                # Valida los datos
                codigo_barras_nuevo = request.POST.get("codigo_barras_nuevo")
                descripcion_nueva = request.POST.get("descripcion_nueva")
                stock_minimo_nuevo = request.POST.get("stock_minimo_nuevo")
                validez2, resultado2 = validar_datos_productos_EDIT(codigo_barras_nuevo, descripcion_nueva, stock_minimo_nuevo)
                if not validez2:
                    return HttpResponse(resultado2)
                
                # Si encuentra un producto que coincide con los 3 datos devuelve un mensaje de error
                consulta = Producto.objects.filter(id=id_producto, codigo_barras=resultado2["codigo_barras"], descripcion=resultado2["descripcion"], stock_minimo=resultado2["stock_minimo"])
                if consulta.exists():
                    return HttpResponse('<p class="text-red-600">No modificaste ningun dato al editar el producto!</p>')
                
                # Verifica si hay otro producto con el mismo codigo de barras o descripcion
                if resultado2["codigo_barras"] is not None:
                    consulta1 = Producto.objects.filter(codigo_barras=resultado2["codigo_barras"]).exclude(id=id_producto).exists()
                    if consulta1:
                        return HttpResponse('<p class="text-red-600">Este codigo de barras esta siendo utilizado por otro producto!</p>')
                consulta2 = Producto.objects.filter(descripcion=resultado2["descripcion"]).exclude(id=id_producto).exists()
                if consulta2:
                    return HttpResponse('<p class="text-red-600">Esta descripcion pertenece a otro producto!</p>')
                
                # Si encuentra un producto con el mismo id modifica los datos
                consulta = Producto.objects.filter(id = id_producto)
                if consulta.exists():
                    consulta.update(
                        codigo_barras=resultado2["codigo_barras"], 
                        descripcion=resultado2["descripcion"], 
                        stock_minimo=resultado2["stock_minimo"]
                        )
                    response = HttpResponse('<p class="text-green-600"> Producto modificado correctamente!</p>')
                    response["HX-Trigger"] = "recargarTabla" # Activa el evento recargar tabla cuando es enviada la respuesta
                    return response
                else:
                    return HttpResponse('<p class="text-red-600">Error al intentar editar un producto: No se a encontrado en la base de datos.</p>')
            except Exception as error:
                return HttpResponse('<p class="text-red-600">Error al intentar editar un producto: '+str(error)+'</p>')
    return redirect('crud_productos')

# ---------------------------------------

# Vistas de modificar_precio_stock
# ---------------------------------------

# MPS = Modificar precio y stock
def recargarTablaHTMX_MPS(request):
    if request.method == "GET":
        if request.headers.get('HX-Request'): 
            # Diccionario con los casos
            ordenamientos = {
                "fechaAscendente": "ultima_fecha_actualizacion_precio",
                "fechaDescendente": "-ultima_fecha_actualizacion_precio",
                "codigoAscendente": "codigo_barras",
                "codigoDescendente": "-codigo_barras",
                "descripcionAscendente": "descripcion",
                "descripcionDescendente": "-descripcion",
                "precioMayor": "-precio",
                "precioMenor": "precio",
                "stockMayor": "-stock",
                "stockMenor": "stock",
            }

            caso = request.GET.get("caso")
            orden = ordenamientos.get(caso)

            if orden: # Si el caso coincide con alguno del diccionario ordena
                productos = Producto.objects.order_by(orden)
            else: # En caso de que no trae asi nomas los productos
                productos = Producto.objects.all()
                print(caso)
                
            return render(request, "productos/partials/tbody_modificar_precio_stock.html", {
                "productos": productos, "metodo": caso
            })

def modificar_precio_stock_CRUD(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):
            try: # Obtiene los datos
                id_producto = request.POST.get("id_producto")
                stock_viejo = request.POST.get("stock_viejo")
                precio_viejo = request.POST.get("precio_viejo")

                stock_nuevo = request.POST.get("stock_nuevo")
                precio_nuevo = request.POST.get("precio_nuevo")

                # Valida el stock nuevo
                validez_stock_nuevo, resultado_stock_nuevo = validar_stock(stock_nuevo)
                if not validez_stock_nuevo:
                    return HttpResponse(resultado_stock_nuevo)
                
                # Valida el precio nuevo
                validez_precio_nuevo, resultado_precio_nuevo = validar_precio(precio_nuevo)
                if not validez_precio_nuevo:
                    return HttpResponse(resultado_precio_nuevo)
                
                # Verifica que el precio nuevo y el stock nuevo no sean iguales a los viejos
                validez_stock_viejo, resultado_stock_viejo = validar_stock(stock_viejo)
                validez_precio_viejo, resultado_precio_viejo = validar_precio(precio_viejo)
                if resultado_stock_nuevo == resultado_stock_viejo and resultado_precio_nuevo == resultado_precio_viejo:
                    return HttpResponse('<p class="text-red-600">No cambiaste el precio ni el stock!</p>')

                # Verifica si existen productos con el mismo id en la base de datos
                consulta = Producto.objects.filter(id=id_producto).update(
                    precio=resultado_precio_nuevo, 
                    stock=resultado_stock_nuevo, 
                    ultima_fecha_actualizacion_precio=timezone.now() # Actualiza la fecha
                    )
                if consulta > 0:
                    # metodo_p = request.POST.get("metodo_p")
                    response = HttpResponse('<p class="text-green-600">Precio y Stock modificados correctamente!</p>')
                    response["HX-Trigger"] = "recargarTablaMPS"
                    return response
                else:
                    return HttpResponse('<p class="text-red-600">ERROR: El producto no existe en la base de datos!</p>')
            except Exception as error:
                return HttpResponse('<p class="text-red-600">Error al intentar editar un producto: '+str(error)+'</p>')
    return redirect('modificar_precio_stock')