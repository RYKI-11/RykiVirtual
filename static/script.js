const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", async () => {
  const message = userInput.value.trim();
  if (!message) return;

  chatBox.innerHTML += `<p><b>Tú:</b> ${message}</p>`;
  userInput.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  chatBox.innerHTML += `<p><b>Ryki:</b> ${data.response}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;
});
