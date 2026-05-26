function mostrar_ordenar_por(){
    const ul = document.getElementById("menu_ordenar")
    ul.classList.toggle("hidden")

    const triangulo = document.getElementById("trianguloMenu")
    triangulo.classList.toggle("-rotate-90")
}

// Cambia el texto cuando elije el metodo de ordenamiento
// Cambia el valor del input #metodo_p para cuando editamos un producto este recarga el metodo de ordenamiento
function cambiar_texto_p(caso){ 
    const p = document.getElementById("metodo_ordenamiento")
    const casoV = document.getElementById("metodo_p")

    switch (caso) {
        case "fechaAscendente": {
            p.textContent = "FECHA: A"
            casoV.value = "fechaAscendente"
            break;
        }
        case "fechaDescendente": {
            p.textContent = "FECHA: D"
            casoV.value = "fechaDescendente"
            break;
        }
        case "codigoAscendente": {
            p.textContent = "COD: A"
            casoV.valuet = "codigoAscendente"
            break;
        }
        case "codigoDescendente": {
            p.textContent = "COD: D"
            casoV.value = "codigoDescendente"
            break;
        }
        case "descripcionAscendente": {
            p.textContent = "DESC: A"
            casoV.value = "descripcionAscendente"
            break;
        }
        case "descripcionDescendente": {
            p.textContent = "DESC: D"
            casoV.value = "descripcionDescendente"
            break;
        }
        case "precioMayor": {
            p.textContent = "PRECIO: D"
            casoV.value = "precioMayor"
            break;
        }
        case "precioMenor": {
            p.textContent = "PRECIO: A"
            casoV.value = "precioMenor"
            break;
        }
        case "stockMayor": {
            p.textContent = "STOCK: D"
            casoV.value = "stockMayor"
            break;
        }
        case "stockMenor": {
            p.textContent = "STOCK: A"
            casoV.value = "stockMenor"
            break;
        }
        default: {
            break;
        }
    }
}