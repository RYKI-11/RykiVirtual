const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    addMessage("Tú", text);
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    addMessage("Ryki", data.response); // 👈 AQUÍ ESTABA EL ERROR
});


function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = "msg";

    div.innerHTML = `<b>${sender}:</b> ${text}`;
    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

