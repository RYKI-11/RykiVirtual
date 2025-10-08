const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// 🔗 Cambia esta URL si la tuya en Render es diferente
const API_URL = "https://rykivirtual.onrender.com/chat";

// Función para agregar mensajes al chat
function addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const content = document.createElement("p");
    content.textContent = text;

    messageDiv.appendChild(content);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Función para enviar el mensaje al servidor
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error("Error al comunicarse con el servidor");
        }

        const data = await response.json();
        const reply = data.response || "Lo siento, no entendí eso 😅";
        addMessage("bot", reply);

    } catch (error) {
        console.error("Error:", error);
        addMessage("bot", "⚠️ Error al conectar con Ryki Virtual. Intenta de nuevo más tarde.");
    }
}

// Enviar al hacer clic en el botón
sendBtn.addEventListener("click", sendMessage);

// Enviar al presionar Enter
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
