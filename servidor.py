from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import wikipedia
from ddgs import DDGS

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

memory = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(data: dict):

    msg = data.get("message","")
    reply = ""

    if msg.lower() == "borrar":
        memory.clear()
        return {"reply":"Memoria borrada"}

    if "wikipedia" in msg.lower():
        try:
            topic = msg.replace("wikipedia","")
            reply = wikipedia.summary(topic, sentences=2)
        except:
            reply = "No encontré eso en Wikipedia"

    elif "buscar" in msg.lower():
        q = msg.replace("buscar","")
        with DDGS() as ddgs:
            r = list(ddgs.text(q,max_results=1))
            reply = r[0]["body"] if r else "No encontré nada"

    else:
        reply = "Entendido: " + msg
        memory.append(msg)

    return {"reply":reply}
