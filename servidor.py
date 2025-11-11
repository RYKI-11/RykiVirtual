from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import wikipedia
from duckduckgo_search import DDGS
import uvicorn
import os
import json

# --------------------------
# Configuración base del servidor
# --------------------------
app = FastAPI()

# Archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("index.html")

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Memoria de conversación
# --------------------------
MEMORIA_PATH = "memoria.json"

if os.path.exists(MEMORIA_PATH):
    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = {}

# --------------------------
# Funciones de búsqueda
# --------------------------
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

# --------------------------
# Ruta principal del chat
# --------------------------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("message", "").strip().lower()
    user_id = data.get("user_id", "default")

    if not mensaje:
        return JSONResponse({"response": "Por favor, escribe algo para que Ryki Virtual pueda responderte."})

    if user_id not in memoria:
        memoria[user_id] = []

    memoria[user_id].append({"usuario": mensaje})

    # Respuestas básicas
    respuestas = {
        "hola": "¡Hola! Soy Ryki Virtual 😊 ¿En qué puedo ayudarte hoy?",
        "cómo estás": "Estoy muy bien, gracias por preguntar. ¿Y tú?",
        "quién te creó": "Fui creada por un desarrollador curioso como tú.",
        "adiós": "¡Hasta pronto! 👋 Espero que vuelvas pronto.",
        "qué puedes hacer": "Puedo responder preguntas, buscar información en Wikipedia y DuckDuckGo, y mantener el contexto de nuestras charlas."
    }

    respuesta = respuestas.get(mensaje)

    if not respuesta:
        respuesta = buscar_wikipedia(mensaje)
        if not respuesta:
            respuesta = buscar_duckduckgo(mensaje)
            if not respuesta:
                respuesta = "Lo siento 😅, no encontré información sobre eso."

    memoria[user_id].append({"ryki": respuesta})

    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

    return JSONResponse({"response": respuesta, "historial": memoria[user_id]})

# --------------------------
# Ejecución en Render
# --------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("servidor:app", host="0.0.0.0", port=port)
