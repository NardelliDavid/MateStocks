function mostrar_confirmacion(EE,id){
    switch (EE) {
        case 1: // CASO 1: Editar
            // Oculta el icono de editar
            const imgEditar = document.getElementById("editarIcono"+id)
            imgEditar.classList.toggle("hidden")

            // Muestra el div que contiene los iconos de confirmar y cancelar
            const divEditar = document.getElementById("confirmacionEditar"+id);
            divEditar.classList.toggle("hidden");
            divEditar.classList.toggle("flex")

            // Oculta las columnas originales
            const tdOriginales = document.querySelectorAll(".prod"+id+"Original")
            tdOriginales.forEach(td => td.classList.toggle("hidden"))

            // Muestra las columnas a editar
            const tdNuevos = document.querySelectorAll(".prod"+id+"Nuevo")
            tdNuevos.forEach(td => td.classList.toggle("hidden"))

            break;
        case 2: // CASO 2: Eliminar
            // Oculta el icono de basura
            const imgEliminar = document.getElementById("basuraIcono"+id)
            imgEliminar.classList.toggle("hidden")

            // Muestra el div que contiene los iconos de confirmar y cancelar
            const divEliminar = document.getElementById("confirmacionEliminar"+id);
            divEliminar.classList.toggle("hidden");
            divEliminar.classList.toggle("flex")
            break;
        default:
            console.log("NO CORRESPONDE A ELIMINAR NI EDITAR")
            break;
    }
}