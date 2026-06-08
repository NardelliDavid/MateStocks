// Calcula el costo total y lo muestra
function costoTotal() {
  const tbodyindex = document.querySelectorAll("#tbodyindex tr");

  // Calcula el costo total
  let costoTotal = 0;
  tbodyindex.forEach((tr) => {
    const precio = parseFloat(
      tr.querySelector(".precioProducto p").textContent,
    );
    const cantidad = parseInt(
      tr.querySelector(".cantidadProducto").textContent,
    );

    costoTotal = costoTotal + precio * cantidad;
  });

  // Inserta el costoTotal en la etiqueta p con ese id
  const costoTotalTexto = document.getElementById("costoTotalTexto");
  costoTotalTexto.textContent = costoTotal
}
