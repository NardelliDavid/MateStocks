#from django.http import HttpResponse
from django.shortcuts import render, redirect
from .validators import *
from django.http import HttpResponse
from apps.productos.models import Producto

# Create your views here.
def index(request):
    sesionProductos = request.session.get("productosDiccionario", [])
    return render(request, "tickets/index.html", {
        "sesionProductos": sesionProductos
    })

# VISTAS PARA EL INDEX
#-------------------------------------------------------

def buscar_producto_ticket(request):
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            codigo_barra = request.GET.get("codigo_barra")
            descripcion = request.GET.get("descripcion")

            # VALIDA EL CODIGO DE BARRAS
            validez_codigo, codigo_barra_validado = validar_codigo_barras(codigo_barra)
            if not validez_codigo:
                return HttpResponse(codigo_barra_validado)
            
            # VALIDA LA DESCRIPCION
            validez_desc, desc_validada = validar_descripcion(descripcion)
            if not validez_desc:
                return HttpResponse(desc_validada)
            
            # VERIFICA QUE CAMPOS ESTAN VACIOS Y CREA LA CONSULTA EN BASE A ESO
            if codigo_barra_validado is None and desc_validada is None:
                return HttpResponse("")
            elif codigo_barra_validado is None:
                producto = Producto.objects.filter(descripcion__icontains=desc_validada)
            elif desc_validada is None:
                producto = Producto.objects.filter(codigo_barras__icontains=codigo_barra_validado)
            else:
                producto = Producto.objects.filter(codigo_barras__icontains=codigo_barra_validado, descripcion__icontains=desc_validada)

            # DEVUELVE LA RESPUESTA AL FRONTEND
            respuesta = '<div class="bg-white w-[100%] max-h-[70px] overflow-auto rounded">'
            if producto.exists():
                for i in producto:
                    respuesta += '<p class="border-b border-gray-200">'+str(i.codigo_barras)+'<br>'+str(i.descripcion)+'</p>'
                respuesta += '</div>'
                return HttpResponse(respuesta)
            else:
                respuesta += "No hay productos que coincidan en la base de datos!</div>"
                return HttpResponse(respuesta)

def agregar_producto_ticket(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):
            codigo_barra = request.POST.get("codigo_barra")
            descripcion = request.POST.get("descripcion")
            cantidad_producto = request.POST.get("cantidad_producto")

            # CANTIDAD DE ETIQUETAS p ADENTRO DEL DIV
            cantidadP= int(request.POST.get("cantidadP"))

            # VALIDA EL CODIGO DE BARRAS
            validez_codigo, codigo_barra_validado = validar_codigo_barras(codigo_barra)
            if not validez_codigo:
                return HttpResponse(codigo_barra_validado)
            
            # VALIDA LA DESCRIPCION
            validez_desc, desc_validada = validar_descripcion(descripcion)
            if not validez_desc:
                return HttpResponse(desc_validada)
            
            # VALIDA LA CANTIDAD DEL PRODUCTO
            validez_cant, cant_validada = validar_cantidad(cantidad_producto)
            if not validez_cant:
                return HttpResponse(cant_validada)
            
            # Si ambos campos estan vacios
            if desc_validada == None and codigo_barra_validado == None:
                return HttpResponse('<p class="text-red-600">Ambos campos estan vacios!</p>')
            
            # Lista el producto agregandolo a las variables de sesion
            if cantidadP == 0: # Si no encuentra productos en la base de datos devuelve un mensaje de error
                return HttpResponse('<p class="text-red-600">No hay productos seleccionados!</p>')
            elif cantidadP != 1: # Si encuentra muchos productos el buscador devuelve un mensaje de error
                return HttpResponse('<p class="text-red-600">Hay demasiados productos seleccionados! Complete la descripcion o codigo hasta que quede uno solo.</p>')
            else: # Si encuentra uno solo lo agrega a la variable de sesion

                # Busca el producto en la base de datos
                if desc_validada != None and codigo_barra_validado != None:
                    consulta = Producto.objects.filter(codigo_barras__icontains=codigo_barra_validado, 
                                                       descripcion__icontains=desc_validada).first()
                elif desc_validada != None and codigo_barra_validado == None:
                    consulta = Producto.objects.filter(descripcion__icontains=desc_validada).first()
                elif desc_validada == None and codigo_barra_validado != None:
                    consulta = Producto.objects.filter(codigo_barras__icontains=codigo_barra_validado).first()
                else:
                    return HttpResponse('<p class="text-red-600">Error</p>')
                
                # Si no encuentra productos
                if consulta is None:
                    return HttpResponse('<p class="text-red-600">Producto no encontrado!</p>')

                # Si el stock es menor a la cantidad solicitada
                if cant_validada > consulta.stock:
                    return HttpResponse('<p class="text-red-600">No hay suficiente stock!</p>')
                
                # Obtiene la variable de sesion productosDiccionario
                sesionProductos = request.session.get("productosDiccionario", []) 
                # Verifica si el producto ya existe en la variable de sesion
                encontrado = False
                for producto in sesionProductos:
                    # Si existe le suma cantidad
                    if producto["codigo_barras"] == consulta.codigo_barras and producto["descripcion"] == consulta.descripcion:
                        cant_total = producto["cantidad"] + cant_validada
                        # Si la cantidad total supera el stock en la base de datos devuelve un mensaje de error
                        if cant_total > consulta.stock:
                            return HttpResponse('<p class="text-red-600">No hay suficiente stock!</p>')
                        else: # En caso contrario aumenta la cantidad
                            producto["cantidad"] = cant_total
                            encontrado = True
                            request.session["productosDiccionario"] = sesionProductos
                            request.session.modified = True
                            break
                
                # Si no encontro el producto en la variable de sesion lo agrega
                if not encontrado:
                    # Crea un diccionario para el producto
                    productoArray = {
                        "id": consulta.id,
                        "codigo_barras": consulta.codigo_barras,
                        "descripcion": consulta.descripcion,
                        "precio": str(consulta.precio),
                        "cantidad": cant_validada,
                        "stock": consulta.stock,
                        "stock_minimo": consulta.stock_minimo
                    }
                    sesionProductos.append(productoArray)
                    request.session["productosDiccionario"] = sesionProductos
                    request.session.modified = True
                
                response = HttpResponse('<p class="text-green-600">Producto agregado correctamente al ticket!</p>')
                response["HX-Trigger"] = "recargarTablaTicket" # Evento para recargar la tabla
                return response


def recargarTablaIndex(request): # EVENTO RECARGAR TABLA AL AGREGAR UN PRODUCTO AL TICKET
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            sesionProductos = request.session.get("productosDiccionario", [])
            return render(request, "tickets/partials/tbody_index.html", {
                "sesionProductos": sesionProductos
            })
        

def quitarProductoDelTicket(request): # Quita el producto del ticket
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            
            idProducto = int(request.GET.get("id"))
            productosTicket = request.session.get('productosDiccionario', [])

            # Creo un array para quitar el producto de la variable de sesion
            nuevoProductosTicket = []
            for producto in productosTicket:
                if producto.get('id') != idProducto:
                    nuevoProductosTicket.append(producto)
            
            
            # Reemplazo el array original por el nuevo
            request.session['productosDiccionario'] = nuevoProductosTicket
            request.session.modified = True

            response = HttpResponse()
            response["HX-Trigger"] = "recargarTablaTicket" # Evento para recargar la tabla
            return response
        
def vaciarTicket(request): # Vacia el ticket que estamos haciendo
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            request.session.flush()

            response = HttpResponse('<p class="text-green-600">Ticket vaciado!</p>')
            response["HX-Trigger"] = "recargarTablaTicket" # Evento para recargar la tabla
            return response
