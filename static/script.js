const input = document.getElementById("userInput");
const send = document.getElementById("sendBtn");
const clear = document.getElementById("clearBtn");
const chat = document.getElementById("chatBox");

send.onclick = sendMsg;
clear.onclick = clearChat;

function add(text,cls){
 let d = document.createElement("div");
 d.className = cls;
 d.innerText = text;
 chat.appendChild(d);
 chat.scrollTop = chat.scrollHeight;
}

async function sendMsg(){

 let msg = input.value;
 if(!msg) return;

 add("Tú: "+msg,"user");
 input.value="";

 let r = await fetch("/chat",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({message:msg})
 });

 let data = await r.json();
 add("Ryki: "+data.reply,"bot");
}

function clearChat(){
 chat.innerHTML="";
}
