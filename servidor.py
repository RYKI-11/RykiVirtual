from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import wikipedia
from duckduckgo_search import DDGS

app = FastAPI()

# Permitir solicitudes desde cualquier origen (por ejemplo, tu página en Render o Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>Ryki Virtual está activo 🧠</h1><p>Usa el chat desde tu página web.</p>"

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    pregunta = data.get("message", "").lower()

    respuesta = "No estoy seguro de eso, pero puedo buscarlo por ti 🔍"

    # Respuestas básicas
    if "hola" in pregunta:
        respuesta = "¡Hola! Soy Ryki Virtual 🤖, ¿en qué puedo ayudarte?"
    elif "cómo estás" in pregunta:
        respuesta = "Estoy genial, gracias por preguntar 😊"
    elif "adiós" in pregunta:
        respuesta = "¡Hasta pronto! 👋"
    elif "tu nombre" in pregunta:
        respuesta = "Me llamo Ryki Virtual 🌐, tu asistente inteligente."
    else:
        try:
            # Intentar buscar en Wikipedia
            resumen = wikipedia.summary(pregunta, sentences=2, auto_suggest=False)
            respuesta = resumen
        except Exception:
            # Si Wikipedia no tiene resultados, usar DuckDuckGo
            try:
                ddgs = DDGS()
                resultado = list(ddgs.text(pregunta, max_results=1))
                if resultado:
                    respuesta = resultado[0]["body"]
            except Exception:
                respuesta = "Lo siento 😅, no encontré información sobre eso."

    return {"response": respuesta}
