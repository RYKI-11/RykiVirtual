const table = document.getElementById("chatTable");
const input = document.getElementById("message");

function addRow(user, bot) {
    const row = document.createElement("tr");

    const td1 = document.createElement("td");
    td1.innerHTML = "<b>Tú:</b> " + user;

    const td2 = document.createElement("td");
    td2.innerHTML = "<b>Ryki:</b> " + bot;

    row.appendChild(td1);
    row.appendChild(td2);
    table.appendChild(row);
}

function send() {
    const text = input.value.trim();
    if (!text) return;

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(r => r.json())
    .then(data => {
        addRow(text, data.response);
        input.value = "";
    });
}

function clearChat() {
    table.innerHTML = "";
}
