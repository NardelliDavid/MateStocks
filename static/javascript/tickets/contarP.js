// CUENTA LA CANTIDAD DE PRODUCTOS ENCONTRADOS PARA MANDAR AL BACKEND
function contarP () {
    const p = document.querySelectorAll("#resultadoBusqueda p")
    cantidadP = p.length
    return cantidadP
}