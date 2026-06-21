from django.shortcuts import render, redirect
from apps.productos.models import Producto
from django.http import HttpResponse
from .validators import *
from django.utils import timezone
from django.views.decorators.cache import never_cache
import openpyxl

@never_cache

# Create your views here.
def crud_productos(request):
    request.session.flush()
    productos = Producto.objects.all()

    return render(request, "productos/crud_productos.html", {
        "productos": productos
    })

def modificar_precio_stock(request):
    request.session.flush()
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
                    return HttpResponse(msgError('Este producto ya existe en la base de datos!'))
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
                    response = HttpResponse(msgCorrecto(str(resultado["descripcion"])+' agregado/s con exito!'))
                    response["HX-Trigger"] = "recargarTabla" # Llama al evento "recargarTabla" cuando la respuesta llega a la plantilla
                    return response
            except Exception as error:
                return HttpResponse(msgError('Error al agregar producto: '+str(error)))
    return redirect('crud_productos')

def eliminar_producto(request):
    if request.method == "POST":
        if request.headers.get('HX-Request'):
            try: # Obtiene el id enviado desde la plantilla
                id_producto = request.POST.get("id_producto") 
                consulta = Producto.objects.filter(id=id_producto)
                if consulta.exists(): # Si encuentra objetos con el mismo ID los borra
                    consulta.delete()
                    response = HttpResponse(msgCorrecto('Producto eliminado correctamente!'))
                    response["HX-Trigger"] = "recargarTabla" # Activa el evento recargar tabla cuando es enviada la respuesta
                else:
                    response = HttpResponse(msgError('Error al intentar eliminar un producto: No se a encontrado en la base de datos.'))
                return response
            except Exception as error:
                return HttpResponse(msgError("ERROR AL ELIMINAR PRODUCTO: "+str(error)))
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
                    return HttpResponse(msgError('No modificaste ningun dato al editar el producto!'))
                
                # Verifica si hay otro producto con el mismo codigo de barras o descripcion
                if resultado2["codigo_barras"] is not None:
                    consulta1 = Producto.objects.filter(codigo_barras=resultado2["codigo_barras"]).exclude(id=id_producto).exists()
                    if consulta1:
                        return HttpResponse(msgError('Este codigo de barras esta siendo utilizado por otro producto!'))
                consulta2 = Producto.objects.filter(descripcion=resultado2["descripcion"]).exclude(id=id_producto).exists()
                if consulta2:
                    return HttpResponse(msgError('Esta descripcion pertenece a otro producto!'))
                
                # Si encuentra un producto con el mismo id modifica los datos
                consulta = Producto.objects.filter(id = id_producto)
                if consulta.exists():
                    consulta.update(
                        codigo_barras=resultado2["codigo_barras"], 
                        descripcion=resultado2["descripcion"], 
                        stock_minimo=resultado2["stock_minimo"]
                        )
                    response = HttpResponse(msgCorrecto(' Producto modificado correctamente!'))
                    response["HX-Trigger"] = "recargarTabla" # Activa el evento recargar tabla cuando es enviada la respuesta
                    return response
                else:
                    return HttpResponse(msgError('Error al intentar editar un producto: No se a encontrado en la base de datos.'))
            except Exception as error:
                return HttpResponse(msgError('Error al intentar editar un producto: '+str(error)))
    return redirect('crud_productos')

def leer_xlsx_con_productos(request): # Obtiene los productos del .xlsx y los carga a la base de datos
    if request.method == "POST":
        if request.headers.get('HX-Request'): 
            try:
                archivo_xlsx = request.FILES['archivo_xlsx']

                # Abrimos el archivo para lectura
                wb = openpyxl.load_workbook(archivo_xlsx, data_only=True)
                hoja = wb.active

                # Recorro el archivo desde la primera fila (columnas A-E)
                productos_nuevos = []
                for fila in hoja.iter_rows(min_row=1, min_col=1, max_col=5, values_only=True):
                    # Ignora las filas completamente vacias
                    if all(v is None for v in fila):
                        continue

                    producto = {
                        "codigo_barras": fila[0],
                        "descripcion": fila[1],
                        "precio": fila[2],
                        "stock": fila[3],
                        "stock_minimo": fila[4]
                    }
                    productos_nuevos.append(producto)
                    
                try:
                    validez, productos_validados = validar_datos_productos_XLSX(productos_nuevos)
                    if not validez:
                        return HttpResponse(msgError("Error al cargar los productos del archivo .xlsx! verifique los datos de cada producto."))
                    
                    # Obtiene todos los códigos del XLSX
                    codigos = [
                        p["codigo_barras"]
                        for p in productos_validados
                        if p["codigo_barras"] is not None
                    ]
                    if len(codigos) != len(set(codigos)): # Verifica que no hayan codigos de barras repetidos en el XLSX
                        return HttpResponse(
                            msgError("Hay códigos de barras repetidos en el archivo XLSX.")
                        )
                    descripciones = [p["descripcion"] for p in productos_validados] # Obtiene todas las descripciones de XLSX
                    if len(descripciones) != len(set(descripciones)): # Verifica que no hayan descripciones repetidas en el XLSX
                        return HttpResponse(
                            msgError("Hay descripciones repetidas en el archivo XLSX.")
                        )

                    # Verifica si existen productos con el mismo codigo de barras o descripcion en la base de datos
                    if (
                        Producto.objects.filter(codigo_barras__in=codigos).exists()
                        or Producto.objects.filter(descripcion__in=descripciones).exists()
                    ):
                        return HttpResponse(
                            msgError("Hay uno o más productos que ya están cargados en la base de datos!")
                        )

                    # Carga todos los productos a la base de datos
                    productos = [
                        Producto(
                            codigo_barras=p["codigo_barras"],
                            descripcion=p["descripcion"],
                            precio=p["precio"],
                            stock=p["stock"],
                            stock_minimo=p["stock_minimo"],
                        )
                        for p in productos_validados
                    ]
                    Producto.objects.bulk_create(productos)
                        
                    # Retorna un mensaje y un evento
                    response = HttpResponse(msgCorrecto("Productos cargados correctamente desde el archivo .xlsx!"))  
                    response["HX-Trigger"] = "recargarTabla"
                    return response
                except Exception as e:
                    return HttpResponse("TODO MAL 2:"+str(e))


            except Exception as e:
                return HttpResponse("TODO MAL:"+str(e))



            return HttpResponse("TODO BIEN:")
    

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
                    return HttpResponse(msgError('No cambiaste el precio ni el stock!'))

                # Verifica si existen productos con el mismo id en la base de datos
                consulta = Producto.objects.filter(id=id_producto).update(
                    precio=resultado_precio_nuevo, 
                    stock=resultado_stock_nuevo, 
                    ultima_fecha_actualizacion_precio=timezone.now() # Actualiza la fecha
                    )
                if consulta > 0:
                    # metodo_p = request.POST.get("metodo_p")
                    response = HttpResponse(msgCorrecto('Precio y Stock modificados correctamente!'))
                    response["HX-Trigger"] = "recargarTablaMPS"
                    return response
                else:
                    return HttpResponse(msgError('ERROR: El producto no existe en la base de datos!'))
            except Exception as error:
                return HttpResponse(msgError('Error al intentar editar un producto: '+str(error)))
    return redirect('modificar_precio_stock')