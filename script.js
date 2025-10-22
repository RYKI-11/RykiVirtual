
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const historyList = document.getElementById("history");

const sessionId = "ryki_session";
let conversations = JSON.parse(localStorage.getItem(sessionId)) || [];

// Mostrar historial previo al cargar
window.addEventListener("load", () => {
  conversations.forEach((msg) => {
    if (msg.user) appendMessage("user", msg.user);
    if (msg.ryki) appendMessage("ryki", msg.ryki);
  });
  updateHistory();
});

// Enviar mensaje
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  conversations.push({ user: message });
  userInput.value = "";
  saveConversations();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    const data = await res.json();
    appendMessage("ryki", data.response);
    conversations.push({ ryki: data.response });
    saveConversations();
    updateHistory();
  } catch (error) {
    appendMessage("ryki", "⚠️ Error de conexión con el servidor.");
  }
}

// Mostrar mensajes en el chat
function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Guardar conversaciones en localStorage
function saveConversations() {
  localStorage.setItem(sessionId, JSON.stringify(conversations));
}

// Actualizar historial lateral
function updateHistory() {
  historyList.innerHTML = "";
  conversations.forEach((msg) => {
    const li = document.createElement("li");
    li.textContent = msg.user || msg.ryki;
    historyList.appendChild(li);
  });
}

// --- EVENTOS ---
// Enviar con clic
sendBtn.addEventListener("click", sendMessage);

// Enviar con Enter (Shift+Enter = salto de línea)
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});
