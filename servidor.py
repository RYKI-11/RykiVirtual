from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import wikipedia
from duckduckgo_search import DDGS
import os

app = FastAPI()

# --- Configuración de Wikipedia ---
wikipedia.set_lang("es")

# --- Montar archivos estáticos (CSS y JS) ---
app.mount("/static", StaticFiles(directory="."), name="static")

# --- Datos básicos del asistente ---
respuestas_basicas = {
    "hola": "¡Hola! Soy Ryki Virtual 😊 ¿en qué puedo ayudarte hoy?",
    "como estas": "Estoy muy bien, ¡gracias por preguntar! ¿y tú?",
    "quien eres": "Soy Ryki Virtual, tu asistente inteligente creado por ti 😎",
    "adios": "¡Hasta luego! Espero verte pronto 👋",
    "que puedes hacer": "Puedo responderte cosas básicas, ayudarte con preguntas de primaria y secundaria, y buscar información en Internet 🔍",
}

# --- Preguntas educativas ---
respuestas_educativas = {
    "que es una fraccion": "Una fracción representa una parte de un todo. Por ejemplo, 1/2 es la mitad de algo.",
    "que es un verbo": "Un verbo es una palabra que indica acción, estado o proceso, como 'correr' o 'ser'.",
    "que es la fotosintesis": "La fotosíntesis es el proceso mediante el cual las plantas convierten la luz solar en energía.",
    "quien descubrio america": "Cristóbal Colón descubrió América en 1492.",
    "que es un circuito electrico": "Un circuito eléctrico es un conjunto de elementos conectados que permiten el paso de corriente eléctrica.",
    "que es el abecedario": "El abecedario es el conjunto de letras que usamos para escribir. En español tiene 27 letras.",
    "que es la informatica": "La informática es la ciencia que estudia el tratamiento automático de la información mediante computadoras.",
    "que es el hardware": "El hardware son las partes físicas de un ordenador, como la pantalla, el teclado o el procesador.",
    "que es el software": "El software son los programas y sistemas que hacen funcionar al hardware, como Windows o una app.",
}

# --- Memoria temporal (recordar conversación) ---
memoria_conversacion = []


# --- Función para buscar en Internet ---
def buscar_internet(pregunta: str) -> str:
    try:
        # Intentar buscar en Wikipedia
        resultado = wikipedia.summary(pregunta, sentences=2)
        return f"Según Wikipedia: {resultado}"
    except Exception:
        # Si no encuentra en Wikipedia, buscar en DuckDuckGo
        try:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(pregunta, region="es-es", max_results=1))
                if resultados:
                    return resultados[0]["body"]
        except Exception:
            pass
    return "No encontré una respuesta clara en Internet 😕"


# --- Endpoint del chat ---
@app.post("/chat")
async def chat(request: Request):
    datos = await request.json()
    pregunta = datos.get("mensaje", "").lower().strip()

    # Guardar en memoria la conversación
    memoria_conversacion.append({"usuario": pregunta})

    respuesta = None

    # Buscar respuestas en los diccionarios
    for clave, valor in {**respuestas_basicas, **respuestas_educativas}.items():
        if clave in pregunta:
            respuesta = valor
            break

    # Si no encontró respuesta, buscar en Internet
    if not respuesta:
        respuesta = buscar_internet(pregunta)

    memoria_conversacion.append({"ryki": respuesta})
    return JSONResponse({"respuesta": respuesta})


# --- Página principal ---
@app.get("/", response_class=HTMLResponse)
async def home():
    ruta_html = os.path.join(os.path.dirname(__file__), "index.html")
    with open(ruta_html, "r", encoding="utf-8") as f:
        return f.read()
