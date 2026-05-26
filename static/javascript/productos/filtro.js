function filtrarProductos(){
    console.log("anda")
    const codigo_barras = document.getElementsByName("codigo_barra")[0].value.toLowerCase()
    const descripcion = document.getElementsByName("descripcion")[0].value.toLowerCase()
    
    const filas = document.querySelectorAll("#tbodyProductos tr")

    filas.forEach(fila => {
        const tds = fila.querySelectorAll("td")

        const td1 = tds[0].textContent.toLowerCase()
        const td2 = tds[2].textContent.toLowerCase()
        
        const coincideCodigoBarras = td1.includes(codigo_barras)
        const coincideDescripcion = td2.includes(descripcion)

        if (coincideCodigoBarras && coincideDescripcion){
            fila.classList.remove("hidden")
        } else {
            fila.classList.add("hidden")
        }
    })
}