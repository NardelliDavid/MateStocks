from decimal import Decimal

# VALIDACIONES POR SEPARADO DE DATOS

def validar_codigo_barras(codigo_barras): # VALIDA EL CODIGO DE BARRAS
    if codigo_barras.strip() == "":
        codigo_barras = None
        return True, codigo_barras
    else:
        if len(codigo_barras.strip()) > 50:
            return False, '<p class="text-red-600">El codigo de barras es demasiado grande!</p>'
        else:
            codigo_barras = codigo_barras.strip().replace(" ","")
            if codigo_barras == "None":
                codigo_barras = None
            return True, codigo_barras

def validar_descripcion(descripcion): # VALIDA LA DESCRIPCION
    if len(descripcion.strip()) > 150:
        return False, '<p class="text-red-600">La descripcion del producto es muy grande!</p>'
    else:
        descripcion = descripcion.strip()
        if descripcion == "":
            descripcion = None
        return True, descripcion

def validar_cantidad(cantidad): # VALIDA EL STOCK
    try:
        cantidad = int(cantidad.replace(" ",""))
        if cantidad <= 0:
            return False, '<p class="text-red-600">La cantidad no puede ser menor a 1!</p>'
        if cantidad > 99999:
            return False, '<p class="text-red-600">La cantidad es demasiado grande!</p>'
        return True, cantidad
    except:
        return False, '<p class="text-red-600">La cantidad es erronea!</p>'