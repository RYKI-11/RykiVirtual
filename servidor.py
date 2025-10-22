from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import wikipedia
from duckduckgo_search import DDGS

# Inicializar FastAPI
app = FastAPI()

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria de conversación por sesión
memorias = {}

# --- Funciones auxiliares ---
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

# --- RUTA PRINCIPAL DEL CHAT ---
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("message", "").lower().strip()
    session_id = data.get("session_id", "default")

    if not mensaje:
        return JSONResponse({"response": "Por favor, escribe algo."})

    if session_id not in memorias:
        memorias[session_id] = []

    memorias[session_id].append({"user": mensaje})

    respuestas = {
        "hola": "¡Hola! Soy Ryki Virtual, tu asistente. ",
        "cómo estás": "Estoy genial, gracias. ¿Y tú?",
        "quién te creó": "Fui creada por un desarrollador curioso como tú .",
        "adiós": "¡Hasta luego! Espero volver a hablar contigo ",
        "qué puedes hacer": "Puedo conversar contigo, responder preguntas, buscar información y aprender del contexto .",
    }

    respuesta = respuestas.get(mensaje)
    if not respuesta:
        respuesta = buscar_wikipedia(mensaje) or buscar_duckduckgo(mensaje)
        if not respuesta:
            respuesta = "Lo siento , no encontré información sobre eso."

    memorias[session_id].append({"ryki": respuesta})

    return JSONResponse({"response": respuesta, "memory": memorias[session_id]})

# --- Servir archivos del frontend ---
app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.get("/")
async def home():
    return FileResponse("index.html")

# --- Iniciar servidor ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("servidor:app", host="0.0.0.0", port=port)
