function mostrarTextoCompleto(id, caso){
    switch (caso) {
        case 1: {
            const div = document.getElementById("mostrarCodigoBarras"+id)
            div.classList.toggle("hidden")
            break;
            }
        case 2: {
            const div = document.getElementById("mostrarDescripcion"+id)
            div.classList.toggle("hidden")
            break;
            }
        default: {
            console.log("No es ninguno de los 2 casos.")
            break;
        }
    }
}