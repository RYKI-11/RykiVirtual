const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const history = document.getElementById("history");

let chats = [];

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    addMessage("Tú", message);
    input.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await res.json();

        // 👇 AQUÍ estaba el fallo
        const reply = data.reply || data.response || "Error del servidor";

        addMessage("Ryki", reply);
        saveHistory(message, reply);

    } catch (err) {
        addMessage("Ryki", "Error conectando con el servidor");
    }
});

function addMessage(user, text) {
    const div = document.createElement("div");
    div.className = user === "Tú" ? "user" : "bot";
    div.innerHTML = `<b>${user}:</b> ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function saveHistory(q, a) {
    chats.push({ q, a });
    renderHistory();
}

function renderHistory() {
    history.innerHTML = "";
    chats.forEach((c, i) => {
        const li = document.createElement("li");
        li.textContent = c.q;
        li.onclick = () => {
            chatBox.innerHTML = "";
            addMessage("Tú", c.q);
            addMessage("Ryki", c.a);
        };
        history.appendChild(li);
    });
}

function clearChat() {
    chats = [];
    chatBox.innerHTML = "";
    history.innerHTML = "";
}

/* ENTER PARA ENVIAR */
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        form.dispatchEvent(new Event("submit"));
    }
});
