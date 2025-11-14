from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import wikipedia
from ddgs import DDGS
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Memoria de chats (persistente mientras el servidor está vivo)
historial = {"chat_1": []}
chat_actual = "chat_1"


def buscar_wikipedia(pregunta):
    try:
        wikipedia.set_lang("es")
        resultado = wikipedia.summary(pregunta, sentences=2)
        return resultado
    except:
        return None


def buscar_duckduckgo(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(pregunta, max_results=2)
        if resultados:
            return resultados[0]["body"]
        return None
    except:
        return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "chats": list(historial.keys()),
            "chat_actual": chat_actual
        }
    )


@app.post("/chat")
async def chat(request: Request, message: str = Form(...)):
    global chat_actual

    respuesta = buscar_wikipedia(message)

    if not respuesta:
        respuesta = buscar_duckduckgo(message)

    if not respuesta:
        respuesta = "No encontré información sobre eso, ¿quieres intentar con otra cosa?"

    historial[chat_actual].append(("user", message))
    historial[chat_actual].append(("bot", respuesta))

    return {"respuesta": respuesta}


@app.post("/cambiar_chat")
async def cambiar_chat(nombre: str = Form(...)):
    global chat_actual

    if nombre not in historial:
        historial[nombre] = []

    chat_actual = nombre
    return {"ok": True}


@app.post("/borrar_chat")
async def borrar_chat(nombre: str = Form(...)):
    global chat_actual

    if nombre in historial:
        del historial[nombre]

    if not historial:
        historial["chat_1"] = []

    chat_actual = list(historial.keys())[0]

    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run("servidor:app", host="0.0.0.0", port=10000)
