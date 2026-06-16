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
  costoTotalTexto.textContent = costoTotal;

  return costoTotal;
}

// Funcion para el costo total y subtotal de cada producto al visualizar un ticket
function actualizarTotalesTicket() {
  const trs = document.querySelectorAll("tbody tr");
  let costoTotal = 0;

  trs.forEach((tr) => {
    const tds = tr.querySelectorAll("td");

    const cantidad = parseInt(tds[1].textContent, 10);
    const precio = parseFloat(tds[2].textContent);

    const subtotal = cantidad * precio;

    tds[3].textContent = subtotal;
    costoTotal += subtotal;
  });

  document.getElementById("costoTotal").textContent =
    `TOTAL: $${costoTotal} ARS`;
}