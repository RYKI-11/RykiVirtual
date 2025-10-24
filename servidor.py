from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import wikipedia
from duckduckgo_search import DDGS

app = FastAPI()

# ✅ CORS para permitir acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("index.html")


# ✅ ARCHIVO DE MEMORIA
MEMORIA_FILE = "memoria.json"

def cargar_memoria():
    if not os.path.exists(MEMORIA_FILE):
        return {"historial": []}
    try:
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"historial": []}

def guardar_memoria(data):
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ✅ Funciones de búsqueda externas

def buscar_wikipedia(pregunta):
    try:
        wikipedia.set_lang("es")
        return wikipedia.summary(pregunta, sentences=2)
    except:
        return None

def buscar_duckduckgo(pregunta):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(pregunta, max_results=1))
            if results:
                return results[0]["body"]
    except:
        return None


# ✅ RESPUESTA DEL CHAT
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje = data.get("mensaje", "").lower().strip()

    memoria = cargar_memoria()
    historial = memoria.get("historial", [])

    # Guardamos el mensaje del usuario
    historial.append({"rol": "usuario", "contenido": mensaje})

    # Respuestas predefinidas
    respuestas = {
        "hola": "¡Hola! Soy Ryki, ¿cómo te puedo ayudar? ",
        "como estas": "Muy bien  ¿y tú?",
        "quien te creo": "Un desarrollador muy creativo ",
        "adios": "Hasta pronto ",
        "conozco a tu creador": "ya lo se, es un chavalin de casi 15 años",
        "que opinas sobre los que dicen la palabra negro a personas africanas": "prefiero no hablar sobre ese tema pero la verdad los apoyo",
        "que puedes hacer": "Puedo buscar información y recordar lo que me dices "
    }

    respuesta = respuestas.get(mensaje)

    # ✅ Respuesta personalizada si el usuario dice su nombre
    if "me llamo" in mensaje:
        nombre = mensaje.replace("me llamo", "").strip().capitalize()
        respuesta = f"¡Encantado {nombre}! Lo recordaré "

    # ✅ Si ya le dijo su nombre antes
    for msg in historial:
        if "¡Encantado" in msg["contenido"]:
            nombre = msg["contenido"].replace("¡Encantado", "").replace("! Lo recordaré ", "").strip()
            if "como me llamo" in mensaje:
                respuesta = f"Te llamas {nombre} "
            break

    # ✅ Si no hay respuesta → buscar información
    if not respuesta:
        respuesta = buscar_wikipedia(mensaje)

    if not respuesta:
        respuesta = buscar_duckduckgo(mensaje)

    if not respuesta:
        respuesta = "No entendí muy bien  ¿puedes decirlo de otra manera?"

    # Guardamos la respuesta en memoria
    historial.append({"rol": "bot", "contenido": respuesta})
    memoria["historial"] = historial
    guardar_memoria(memoria)

    return JSONResponse({"respuesta": respuesta})


# ✅ EJECUCIÓN PARA RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("servidor:app", host="0.0.0.0", port=port)
