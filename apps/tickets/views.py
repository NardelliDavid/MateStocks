#from django.http import HttpResponse
from django.shortcuts import render, redirect
from .validators import *
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from apps.productos.models import Producto
from apps.tickets.models import Tickets, Detalle_ticket
from django.db import transaction
from django.db.models import F

@never_cache

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
                    respuesta += (f'<p '
                                  f'onclick="autocompletar_busqueda(\'{i.codigo_barras}\',\'{i.descripcion}\')" '
                                  f'class="border-b border-gray-200 cursor-pointer hover:bg-gray-100">'+str(i.codigo_barras)+'<br>'+str(i.descripcion)+'</p>')
                    
                return HttpResponse(respuesta)
            else:
                respuesta += "No hay productos que coincidan en la base de datos!</div>"
                return HttpResponse(respuesta)
            
    return redirect("/")

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
                return HttpResponse(msgError("Ambos campos estan vacios!"))
            
            # Lista el producto agregandolo a las variables de sesion
            if cantidadP == 0: # Si no encuentra productos en la base de datos devuelve un mensaje de error
                return HttpResponse(msgError("No hay productos seleccionados!"))
            elif cantidadP != 1: # Si encuentra muchos productos el buscador devuelve un mensaje de error
                return HttpResponse(msgError("Hay demasiados productos seleccionados! Complete la descripcion o codigo hasta que quede uno solo"))
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
                    return HttpResponse(msgError("Error"))
                
                # Si no encuentra productos
                if consulta is None:
                    return HttpResponse(msgError("Producto no encontrado!"))

                # Si el stock es menor a la cantidad solicitada
                if cant_validada > consulta.stock:
                    return HttpResponse(msgError("No hay suficiente stock!"))
                
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
                            return HttpResponse(msgError("No hay suficiente stock!"))
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
                
                response = HttpResponse(msgCorrecto("Producto agregado correctamente al ticket!"))
                response["HX-Trigger"] = "recargarTablaTicket" # Evento para recargar la tabla
                return response
            
    return redirect("/")


def recargarTablaIndex(request): # EVENTO RECARGAR TABLA AL AGREGAR UN PRODUCTO AL TICKET
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            sesionProductos = request.session.get("productosDiccionario", [])
            return render(request, "tickets/partials/tbody_index.html", {
                "sesionProductos": sesionProductos
            })
    
    return redirect("/")

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
        
    return redirect("/")
        
def vaciarTicket(request): # Vacia el ticket que estamos haciendo
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            request.session.flush()

            response = HttpResponse(msgCorrecto("Ticket vaciado!"))
            response["HX-Trigger"] = "recargarTablaTicket" # Evento para recargar la tabla
            return response
        
    return redirect("/")



# VISTAS PARA EL TICKET CREADO
#-------------------------------------------------------

def ticketCreado(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):

            productosTicket = request.session.get('productosDiccionario', [])
            if productosTicket == []:
                return HttpResponse(msgError("No hay productos agregados al ticket!"))
    
            # Verifico el Stock de cada producto
        
            stockModificado = False
            msgStock = 'No hay suficiente stock de: <br>'
            for producto in productosTicket:
                stockDB = Producto.objects.get(id=producto["id"])

                if stockDB.stock < producto["cantidad"]:
                    msgStock += str(producto["descripcion"])+'<br>'
                    stockModificado = True
            msgStock = msgError(msgStock)

            # Si hay productos que tienen menos stock del solicitado devuelve un mensaje de error
            if stockModificado == True:
                return HttpResponse(msgStock)
            else: # Caso contrario crea el ticket
                metodoPago = request.POST.get("metodoPago")
                costoTotal = Decimal(request.POST.get("costoTotal"))
                
                with transaction.atomic():
                    # Crea el ticket
                    ticket = Tickets.objects.create(
                        metodo_pago = metodoPago,
                        total = costoTotal
                    )
                    # Crea los detalles del ticket
                    for producto in productosTicket:
                        Detalle_ticket.objects.create(
                            id_ticket = ticket.id,
                            codigo_barras = producto["codigo_barras"],
                            descripcion = producto["descripcion"],
                            cantidad = producto["cantidad"],
                            precio_unitario = Decimal(producto["precio"])
                        )
                    # Reduce el stock en la base de datos
                    for producto in productosTicket:
                        Producto.objects.filter(id=producto["id"]).update(stock=F('stock') - producto["cantidad"])
                        
                request.session.flush()

                response = HttpResponse()
                response['HX-Redirect'] = f'tickets/verTicket/{ticket.id}'
                return response
            
# VISTA PARA VER LOS TICKETS            
def verTicket(request, id_ticket):
    if request.method == "GET":

        ticket = Tickets.objects.get(id=id_ticket)
        detalles_ticket = Detalle_ticket.objects.filter(id_ticket=id_ticket)

        return render(request, "tickets/verTicket.html", {
            "ticket": ticket,
            "detalles_ticket": detalles_ticket
        })
    
def historial_tickets(request):
    if request.method == "GET":
        tickets = Tickets.objects.all().order_by('-fecha_y_hora')

        return render(request, "tickets/historial_tickets.html", {
            "tickets": tickets
        })
    
def recargarTabla_tickets(request): # Para recargar la tabla mediante HTMX y ver los productos ordenados
    if request.method == "GET":
        if request.headers.get('HX-Request'):
            ordenamientos = {
                "fechaAscendente": "fecha_y_hora",
                "fechaDescendente": "-fecha_y_hora",
                "totalMayor":"total",
                "totalMenor":"-total"
            }

            caso = request.GET.get("caso")
            orden = ordenamientos.get(caso)

            if orden:
                tickets = Tickets.objects.all().order_by(orden)
            else:
                tickets = Tickets.objects.all()

            return render(request, "tickets/partials/tbody_historial_tickets.html", {
                "tickets": tickets
            })
        
def descargar_ticket(request, id_ticket):
    ticket = Tickets.objects.get(id=id_ticket)
    detalles_ticket = Detalle_ticket.objects.filter(id_ticket=id_ticket)

    return render(request, 'tickets/partials/descargar_ticket.html', {
        "ticket": ticket,
        "detalles_ticket": detalles_ticket
    })
    
    


    
