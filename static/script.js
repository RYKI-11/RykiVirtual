const form=document.getElementById("chat-form");
const input=document.getElementById("msg");
const chatBox=document.getElementById("chat-box");
const history=document.getElementById("history");

loadMemory();

form.addEventListener("submit",async e=>{
e.preventDefault();

let text=input.value.trim();
if(!text)return;

add("Tú",text);
input.value="";

const res=await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:text})
});

const data=await res.json();
add("Ryki",data.reply);
loadMemory();
});

async function loadMemory(){
const r=await fetch("/memory");
const d=await r.json();

history.innerHTML="";
d.forEach((c,i)=>{
let li=document.createElement("li");
li.textContent=c[0];
li.onclick=()=>{
chatBox.innerHTML="";
add("Tú",c[0]);
add("Ryki",c[1]);
}
history.appendChild(li);
});
}

function add(who,msg){
let div=document.createElement("div");
div.className=who==="Tú"?"user":"bot";
div.innerHTML=`<b>${who}:</b> ${msg}`;
chatBox.appendChild(div);
chatBox.scrollTop=chatBox.scrollHeight;
}

async function clearChat(){
await fetch("/clear");
history.innerHTML="";
chatBox.innerHTML="";
}

/* ENTER */
input.addEventListener("keydown",e=>{
if(e.key==="Enter"&&!e.shiftKey){
e.preventDefault();
form.dispatchEvent(new Event("submit"));
}
});

