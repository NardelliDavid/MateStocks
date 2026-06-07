function decrecer_valor(){
    const inputN = document.getElementById("cantidad_producto")
    const inputValor = parseInt(inputN.value)
    if (inputValor <= 1) {
        console.log("EL VALOR NO PUEDE SER MENOR A 1")
    } else {
        inputN.value = (inputN.value || 2) - 1
    }
}

function crecer_valor(){
    const inputN = document.getElementById("cantidad_producto")
    const inputValor = parseInt(inputN.value)
    inputN.value = (inputValor || 0) + 1
}