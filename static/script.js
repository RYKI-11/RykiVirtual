
const input = document.getElementById("userInput");
const messages = document.getElementById("messages");
const clearBtn = document.getElementById("clearBtn");

function agregarMensaje(texto, tipo) {
    const msg = document.createElement("div");
    msg.classList.add("message", tipo);
    msg.textContent = texto;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

async function enviarMensaje() {
    const mensaje = input.value.trim();
    if (!mensaje) return;

    agregarMensaje(mensaje, "user");
    input.value = "";

    const res = await fetch("https://rykivirtual.onrender.com/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mensaje})
    });

    const data = await res.json();
    agregarMensaje(data.respuesta, "bot");
}

// ✅ Enviar con ENTER
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") enviarMensaje();
});

// ✅ Botón borrar memoria
clearBtn.addEventListener("click", async () => {
    await fetch("https://rykivirtual.onrender.com/memoria", {
        method: "DELETE"
    });
    messages.innerHTML = "";
    agregarMensaje("Memoria borrada ✅", "bot");
});
