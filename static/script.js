
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const chatHistory = document.getElementById("chat-history");

let conversations = [];
let currentChat = [];

// Función para mostrar mensajes en pantalla
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add(sender === "user" ? "user-message" : "bot-message");
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Enviar mensaje
async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    addMessage(data.response, "bot");

    // Guardar conversación
    currentChat.push({ user: message, bot: data.response });
  } catch {
    addMessage("Error al conectar con el servidor.", "bot");
  }
}

// Enviar con botón
sendBtn.addEventListener("click", sendMessage);

// Enviar con ENTER
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Guardar conversación en la barra lateral
window.addEventListener("beforeunload", () => {
  if (currentChat.length > 0) {
    conversations.push(currentChat);
    const li = document.createElement("li");
    li.textContent = `Chat ${conversations.length}`;
    li.addEventListener("click", () => {
      chatBox.innerHTML = "";
      currentChat.forEach((msg) => {
        addMessage(msg.user, "user");
        addMessage(msg.bot, "bot");
      });
    });
    chatHistory.appendChild(li);
  }
});
