function filtrarProductos(columnaCodigo_barra, columnaDescripcion){
    const codigo_barras = document.getElementsByName("codigo_barra")[0].value.toLowerCase().trim()
    const descripcion = document.getElementsByName("descripcion")[0].value.toLowerCase().trim()
    
    const filas = document.querySelectorAll("#tbodyProductos tr")

    filas.forEach(fila => {
        const tds = fila.querySelectorAll("td")
        console.log(tds.length)
        const td1 = tds[columnaCodigo_barra].textContent.toLowerCase()
        const td2 = tds[columnaDescripcion].textContent.toLowerCase()
        
        const coincideCodigoBarras = td1.includes(codigo_barras)
        const coincideDescripcion = td2.includes(descripcion)

        if (coincideCodigoBarras && coincideDescripcion){
            fila.classList.remove("hidden")
        } else {
            fila.classList.add("hidden")
        }
    })
}