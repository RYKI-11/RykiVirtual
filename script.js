document.getElementById("send-btn").addEventListener("click", enviarMensaje);
document.getElementById("user-input").addEventListener("keypress", function(e) {
  if (e.key === "Enter") enviarMensaje();
});

async function enviarMensaje() {
  const input = document.getElementById("user-input");
  const mensaje = input.value.trim();
  const modo = document.getElementById("mode-selector").value;

  if (!mensaje) return;

  mostrarMensaje("user", mensaje);
  input.value = "";

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: mensaje, mode: modo })
    });

    const data = await res.json();
    mostrarMensaje("bot", data.reply);
  } catch {
    mostrarMensaje("bot", " Error: No puedo conectarme al servidor. Asegúrate de que esté encendido.");
  }
}

function mostrarMensaje(tipo, texto) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", tipo);
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerText = texto;
  msgDiv.appendChild(bubble);
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}
