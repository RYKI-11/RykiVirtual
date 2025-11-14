const input = document.getElementById("message");
const sendBtn = document.getElementById("send");
const chatBox = document.getElementById("chat-box");

const btnNuevoChat = document.getElementById("nuevo-chat");
const btnBorrarChat = document.getElementById("borrar-chat");
const listaChats = document.querySelectorAll(".chat-item");

function agregarMensaje(tipo, texto) {
    const div = document.createElement("div");
    div.className = tipo === "user" ? "msg user" : "msg bot";
    div.textContent = texto;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", enviarMensaje);
input.addEventListener("keypress", e => {
    if (e.key === "Enter") enviarMensaje();
});

function enviarMensaje() {
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje("user", texto);
    input.value = "";

    const formData = new FormData();
    formData.append("message", texto);

    fetch("/chat", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            agregarMensaje("bot", data.respuesta);
        });
}

// Cambiar chat
listaChats.forEach(item => {
    item.addEventListener("click", () => {
        const nombre = item.dataset.nombre;

        const fd = new FormData();
        fd.append("nombre", nombre);

        fetch("/cambiar_chat", { method: "POST", body: fd })
            .then(() => location.reload());
    });
});

// Crear nuevo chat
btnNuevoChat.addEventListener("click", () => {
    const nombre = "chat_" + Math.floor(Math.random() * 9999);

    const fd = new FormData();
    fd.append("nombre", nombre);

    fetch("/cambiar_chat", { method: "POST", body: fd })
        .then(() => location.reload());
});

// Borrar chat
btnBorrarChat.addEventListener("click", () => {
    const nombre = chatActual;
    const fd = new FormData();
    fd.append("nombre", nombre);

    fetch("/borrar_chat", { method: "POST", body: fd })
        .then(() => location.reload());
});
