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
    if descripcion.strip() == "":
        return False, '<p class="text-red-600">La descripcion del producto esta vacia!</p>'
    else:
        if len(descripcion.strip()) > 150:
            return False, '<p class="text-red-600">La descripcion del producto es muy grande!</p>'
        else:
            descripcion = descripcion.strip()
            return True, descripcion

def validar_precio(precio): # VALIDA EL PRECIO
    try:
        precio = Decimal(precio.replace(" ",""))
        if precio <= 0:
            return False, '<p class="text-red-600">El precio no puede ser negativo!</p>'
        if precio > Decimal("99999999.99"):
            return False, '<p class="text-red-600">El precio es demasiado grande!</p>'
        return True, precio
    except:
        return False, '<p class="text-red-600">El precio esta vacio o es erroneo! Utilize puntos en vez de comas para marcar decimales!</p>'
     
def validar_stock(stock): # VALIDA EL STOCK
    try:
        stock = int(stock.replace(" ",""))
        if stock < 0:
            return False, '<p class="text-red-600">El stock no puede ser negativo!</p>'
        if stock > 99999:
            return False, '<p class="text-red-600">El stock es demasiado grande!</p>'
        return True, stock
    except:
        return False, '<p class="text-red-600">El stock esta vacio o es erroneo!</p>'

def validar_stock_minimo(stock_minimo): # VALIDA EL STOCK MINIMO
    try:
        stock_minimo = int(stock_minimo.replace(" ",""))
        if stock_minimo <= 0:
            return False, '<p class="text-red-600">El stock minimo no puede ser negativo!</p>'
        if stock_minimo > 99999:
            return False, '<p class="text-red-600">El stock minimo es demasiado grande!</p>'
        return True, stock_minimo
    except:
        return False, '<p class="text-red-600">El stock minimo esta vacio o es erroneo!</p>'
    
# ------------------------------------------------------------------------------------------

def validar_datos_productos_CREATE(codigo_barras, descripcion, precio, stock, stock_minimo): 
    # REALIZA LAS VALIDACIONES
    validez_codigo_barras, resultado_codigo_barras =  validar_codigo_barras(codigo_barras)
    if not validez_codigo_barras:
        return False, resultado_codigo_barras
    validez_descripcion, resultado_descripcion = validar_descripcion(descripcion)
    if not validez_descripcion:
        return False, resultado_descripcion
    validez_precio, resultado_precio = validar_precio(precio)
    if not validez_precio:
        return False, resultado_precio
    validez_stock, resultado_stock = validar_stock(stock)
    if not validez_stock:
        return False, resultado_stock
    validez_stock_minimo, resultado_stock_minimo = validar_stock_minimo(stock_minimo)
    if not validez_stock_minimo:
        return False, resultado_stock_minimo

    # RETORNA LOS DATOS LIMPIOS
    datos_limpios = {
        "codigo_barras": resultado_codigo_barras,
        "descripcion": resultado_descripcion,
        "precio": resultado_precio,
        "stock": resultado_stock,
        "stock_minimo": resultado_stock_minimo
    }
    return True, datos_limpios

def validar_datos_productos_EDIT(codigo_barras, descripcion,stock_minimo):
    # REALIZA LAS VALIDACIONES
    validez_codigo_barras, resultado_codigo_barras =  validar_codigo_barras(codigo_barras)
    if not validez_codigo_barras:
        return False, resultado_codigo_barras
    validez_descripcion, resultado_descripcion = validar_descripcion(descripcion)
    if not validez_descripcion:
        return False, resultado_descripcion
    validez_stock_minimo, resultado_stock_minimo = validar_stock_minimo(stock_minimo)
    if not validez_stock_minimo:
        return False, resultado_stock_minimo
    
    datos_limpios = {
        "codigo_barras": resultado_codigo_barras,
        "descripcion": resultado_descripcion,
        "stock_minimo": resultado_stock_minimo
    }

    return True, datos_limpios