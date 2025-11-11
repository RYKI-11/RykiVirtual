const botonBuscar = document.getElementById("search-button");
const inputBusqueda = document.getElementById("search-input");
const contenedorResultados = document.getElementById("results");

const API_URL = "https://tu-nombre-de-app-en-render.onrender.com"; // 🔹 cambia esto por tu URL real de Render

async function buscar() {
    const consulta = inputBusqueda.value.trim();
    if (!consulta) return;

    contenedorResultados.innerHTML = "<p>🔄 Buscando...</p>";

    try {
        const respuesta = await fetch(`${API_URL}/buscar?query=${encodeURIComponent(consulta)}`);
        const datos = await respuesta.json();

        contenedorResultados.innerHTML = "";
        datos.resultados.forEach(r => {
            const div = document.createElement("div");
            div.classList.add("resultado");
            div.innerHTML = `
                <h3>${r.titulo}</h3>
                <p>${r.contenido}</p>
                ${r.url ? `<a href="${r.url}" target="_blank">Ver más</a>` : ""}
                <span class="fuente">Fuente: ${r.fuente}</span>
            `;
            contenedorResultados.appendChild(div);
        });
    } catch (error) {
        contenedorResultados.innerHTML = "<p>❌ Error al conectar con el servidor.</p>";
        console.error(error);
    }
}

// 🔹 Ejecutar búsqueda al hacer clic
botonBuscar.addEventListener("click", buscar);

// 🔹 Ejecutar búsqueda al presionar Enter
inputBusqueda.addEventListener("keypress", e => {
    if (e.key === "Enter") buscar();
});
