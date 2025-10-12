from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import wikipedia
from duckduckgo_search import DDGS
import os

app = FastAPI()

# Permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (index.html, style.css, script.js)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    pregunta = data.get("message", "").lower()

    respuesta = "No estoy seguro de eso, pero puedo buscarlo por ti "

    if "hola" in pregunta:
        respuesta = "¡Hola! Soy Ryki Virtual , ¿en qué puedo ayudarte?"
    elif "cómo estás" in pregunta:
        respuesta = "Estoy genial, gracias por preguntar "
    elif "adiós" in pregunta:
        respuesta = "¡Hasta pronto! "
    elif "tu nombre" in pregunta:
        respuesta = "Me llamo Ryki Virtual , tu asistente inteligente."
    else:
        try:
            resumen = wikipedia.summary(pregunta, sentences=2, auto_suggest=False)
            respuesta = resumen
        except Exception:
            try:
                ddgs = DDGS()
                resultado = list(ddgs.text(pregunta, max_results=1))
                if resultado:
                    respuesta = resultado[0]["body"]
            except Exception:
                respuesta = "Lo siento , no encontré información sobre eso."

    return {"response": respuesta}

