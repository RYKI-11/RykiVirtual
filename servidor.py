from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import wikipedia
from duckduckgo_search import DDGS

# Inicializar FastAPI
app = FastAPI()

# Permitir peticiones desde cualquier origen (necesario para el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria de conversación
memory = []

# Función para buscar en Wikipedia
def buscar_wikipedia(pregunta):
    try:
        wikipedia.set_lang("es")
        resumen = wikipedia.summary(pregunta, sentences=2)
        return resumen
    except:
        return None

# Función para buscar en DuckDuckGo
def buscar_duckduckgo(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=1))
            if resultados:
                return resultados[0]["body"]
    except:
        return None

# Respuesta principal del asistente
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("message", "").lower().strip()

    if not mensaje:
        return JSONResponse({"response": "Por favor, escribe algo para que Ryki Virtual pueda responderte"})

    # Añadir mensaje a la memoria
    memory.append({"user": mensaje})

    # Respuestas básicas
    respuestas = {
        "hola": "¡Hola! Soy Ryki Virtual  ¿en qué puedo ayudarte hoy?",
        "cómo estás": "Estoy genial, gracias por preguntar. ¿Y tú?",
        "quién te creó": "Fui creado por un desarrollador curioso como tú .",
        "adiós": "¡Hasta luego!  Espero que vuelvas pronto.",
        "qué puedes hacer": "Puedo responder preguntas básicas, buscar información y ayudarte a aprender .",
        "abc": "El abecedario es: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ, O, P, Q, R, S, T, U, V, W, X, Y, Z."
    }

    respuesta = respuestas.get(mensaje)

    if not respuesta:
        # Intentar buscar en Wikipedia
        respuesta = buscar_wikipedia(mensaje)
        if not respuesta:
            # Si Wikipedia no tiene nada, buscar en DuckDuckGo
            respuesta = buscar_duckduckgo(mensaje)
            if not respuesta:
                respuesta = "Lo siento , no encontré información sobre eso."

    # Añadir respuesta a la memoria
    memory.append({"ryki": respuesta})

    return JSONResponse({"response": respuesta, "memory": memory})


# -------------------------------
# CORRECCIÓN PARA RENDER (PUERTO)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render asigna el puerto automáticamente
    uvicorn.run("servidor:app", host="0.0.0.0", port=port)
