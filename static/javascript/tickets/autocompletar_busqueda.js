function autocompletar_busqueda(codigo_barras, descripcion) {
    const cod = document.getElementById("input-codigoBarras");
    const desc = document.getElementById("input-descripcion");

    cod.value = codigo_barras
    desc.value = descripcion

    // Ejecuta los eventos al buscar un producto
    htmx.trigger(desc, 'change')
    htmx.trigger(cod, "change");
}

// Funcion para limpiar los inputs
function limpiar_input(caso) {
    switch(caso) {
        case 1:
            const desc = document.getElementById("input-descripcion");
            desc.value = ""
            htmx.trigger(desc, "change");
            break;
        case 2:
            const cod = document.getElementById("input-codigoBarras");
            cod.value = ""
            htmx.trigger(cod, "change");
            break;
        default:
            break;
    }
}