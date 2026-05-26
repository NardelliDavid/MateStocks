function mostrar_ordenar_por(){
    const ul = document.getElementById("menu_ordenar")
    ul.classList.toggle("hidden")

    const triangulo = document.getElementById("trianguloMenu")
    triangulo.classList.toggle("-rotate-90")
}

function cambiar_texto_p(caso){ // Cambia el texto cuando elije el metodo de ordenamiento
    const p = document.getElementById("metodo_ordenamiento")

    switch (caso) {
        case "fechaAscendente": {
            p.textContent = "FECHA: A"
            break;
        }
        case "fechaDescendente": {
            p.textContent = "FECHA: D"
            break;
        }
        case "codigoAscendente": {
            p.textContent = "COD: A"
            break;
        }
        case "codigoDescendente": {
            p.textContent = "COD: D"
            break;
        }
        case "descripcionAscendente": {
            p.textContent = "DESC: A"
            break;
        }
        case "descripcionDescendente": {
            p.textContent = "DESC: D"
            break;
        }
        case "precioMayor": {
            p.textContent = "PRECIO: D"
            break;
        }
        case "precioMenor": {
            p.textContent = "PRECIO: A"
            break;
        }
        case "stockMayor": {
            p.textContent = "STOCK: D"
            break;
        }
        case "stockMenor": {
            p.textContent = "STOCK: A"
            break;
        }
        default: {
            break;
        }
    }
}