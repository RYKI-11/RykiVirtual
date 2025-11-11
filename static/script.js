document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("message");
  const chatBox = document.getElementById("chat-box");
  const clearButton = document.getElementById("clear-chat");

  if (!form || !input || !chatBox) {
    console.error("⚠️ Error: Elementos del DOM no encontrados.");
    return;
  }

  // Enviar mensaje
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    appendMessage("Tú", message);
    input.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          user_id: "usuario_demo",
        }),
      });

      const data = await response.json();
      appendMessage("Ryki Virtual", data.response);
    } catch (err) {
      appendMessage("Ryki Virtual", "❌ Error al conectar con el servidor.");
      console.error(err);
    }
  });

  // Enviar con ENTER
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });

  // Botón de borrar conversación
  if (clearButton) {
    clearButton.addEventListener("click", () => {
      chatBox.innerHTML = "";
    });
  }

  // Mostrar mensajes
  function appendMessage(sender, message) {
    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
