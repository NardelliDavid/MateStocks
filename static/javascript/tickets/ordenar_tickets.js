function mostrar_ordenar_por() {
  const ul = document.getElementById("menu_ordenar");
  ul.classList.toggle("hidden");

  const triangulo = document.getElementById("trianguloMenu");
  triangulo.classList.toggle("-rotate-90");
}

function cambiar_texto_p(caso) {
  const p = document.getElementById("metodo_ordenamiento");
  const casoV = document.getElementById("metodo_p");

  switch (caso) {
    case "fechaAscendente": {
      p.textContent = "FECHA: A";
      casoV.value = "fechaAscendente";
      break;
    }
    case "fechaDescendente": {
      p.textContent = "FECHA: D";
      casoV.value = "fechaDescendente";
      break;
    }
    case "totalMayor": {
      p.textContent = "TOTAL: D";
      casoV.value = "totalMayor";
      break;
    }
    case "totalMenor": {
      p.textContent = "TOTAL: A";
      casoV.value = "totalMenor";
      break;
    }
    default: {
      break;
    }
  }
}