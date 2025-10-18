from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import wikipedia
from duckduckgo_search import DDGS

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Memoria de conversación
memory = []

def buscar_wikipedia(pregunta):
    try:
        wikipedia.set_lang("es")
        return wikipedia.summary(pregunta, sentences=2)
    except:
        return None

def buscar_duckduckgo(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=1))
            if resultados:
                return resultados[0]["body"]
    except:
        return None

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("message", "").lower().strip()

    if not mensaje:
        return JSONResponse({"response": "Por favor, escribe algo para que Ryki Virtual pueda responderte."})

    memory.append({"user": mensaje})

    respuestas = {
        "hola": "¡Hola! Soy Ryki Virtual, ¿en qué puedo ayudarte hoy?",
        "cómo estás": "Estoy genial, gracias por preguntar. ¿Y tú?",
        "quién te creó": "Fui creado por un desarrollador curioso como tú 😄.",
        "adiós": "¡Hasta luego! Espero que vuelvas pronto.",
        "qué puedes hacer": "Puedo responder preguntas básicas, buscar información y ayudarte a aprender 🧠.",
    }

    respuesta = respuestas.get(mensaje)

    if not respuesta:
        respuesta = buscar_wikipedia(mensaje) or buscar_duckduckgo(mensaje) or "Lo siento, no encontré información sobre eso."

    memory.append({"ryki": respuesta})
    return JSONResponse({"response": respuesta, "memory": memory})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("servidor:app", host="0.0.0.0", port=port)
