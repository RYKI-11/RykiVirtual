from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import wikipedia
from ddgs import DDGS
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

wikipedia.set_lang("es")

respuestas = [
 "Interesante 🤔",
 "Cuéntame más",
 "Eso suena bien",
 "Entiendo",
 "Vaya 😮",
 "Genial!"
]

def es_pregunta(texto):
    palabras = ["quien","qué","cuando","donde","por que","cómo","cuál"]
    return texto.endswith("?") or any(p in texto for p in palabras)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(data: dict):

    msg = data.get("message","").lower()

    # SI ES PREGUNTA → BUSCAR
    if es_pregunta(msg):
        try:
            reply = wikipedia.summary(msg, sentences=2)
        except:
            with DDGS() as ddgs:
                r = list(ddgs.text(msg,max_results=1))
                reply = r[0]["body"] if r else "No encontré información"

    # SI NO → RESPUESTA NORMAL
    else:
        reply = random.choice(respuestas)

    return {"reply":reply}
