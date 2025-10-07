from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import wikipedia
from duckduckgo_search import DDGS
import json
import os
import datetime

# --- CONFIGURACIÓN ---
wikipedia.set_lang("es")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CLASE PARA LOS MENSAJES ---
class Message(BaseModel):
    message: str
    mode: str

# --- ARCHIVOS DE MEMORIA ---
MEMORIA_FILE = "memoria.json"
INFO_FILE = "info_memoria.json"

# --- FUNCIONES DE MEMORIA ---
def borrar_memoria():
    """Borra la memoria completamente"""
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)
    with open(INFO_FILE, "w", encoding="utf-8") as f:
        json.dump({"ultima_limpieza": str(datetime.date.today())}, f)

def cargar_memoria():
    """Carga la memoria y la fecha de última limpieza"""
    if not os.path.exists(MEMORIA_FILE):
        borrar_memoria()

    with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
        memoria = json.load(f)

    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, "r", encoding="utf-8") as f:
            info = json.load(f)
    else:
        info = {"ultima_limpieza": str(datetime.date.today())}
        with open(INFO_FILE, "w", encoding="utf-8") as f:
            json.dump(info, f)

    return memoria, info

def guardar_memoria(memoria):
    """Guarda la memoria actual"""
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

# --- CARGAR MEMORIA INICIAL ---
memoria, info = cargar_memoria()

# --- BORRAR SI PASÓ UN DÍA ---
hoy = datetime.date.today()
ultima = datetime.date.fromisoformat(info["ultima_limpieza"])
if hoy > ultima:
    borrar_memoria()
    memoria, info = cargar_memoria()
    print("🧹 Memoria limpiada automáticamente (nuevo día).")

# --- FUNCIONES DE BÚSQUEDA ---
def buscar_wikipedia(pregunta):
    try:
        resultados = wikipedia.search(pregunta, results=1)
        if resultados:
            return wikipedia.summary(resultados[0], sentences=2)
        return ""
    except:
        return ""

def buscar_duckduckgo(pregunta):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pregunta, max_results=1))
            if resultados:
                return resultados[0]["body"]
        return ""
    except:
        return ""

# --- FUNCIONES DE MEMORIA ---
def recordar(texto):
    """Añade texto a la memoria global"""
    memoria.append(texto)
    guardar_memoria(memoria)

def obtener_tema_anterior():
    """Devuelve el último tema mencionado"""
    for frase in reversed(memoria):
        if frase.startswith("Usuario: "):
            return frase.replace("Usuario: ", "")
    return None

# --- RESPUESTAS BÁSICAS ---
respuestas = {
    "hola": "¡Hola! Soy Ryki , tu asistente virtual .",
    "como estas": "Estoy muy bien, ¡gracias por preguntar! ",
    "adios": "¡Hasta pronto! ",
    "quien eres": "Soy Ryki Virtual, un asistente que aprende de todos .",
}

# --- ENDPOINT PRINCIPAL ---
@app.post("/chat")
def chat(msg: Message):
    texto = msg.message.lower().strip()
    recordar(f"Usuario: {texto}")

    # --- Respuestas directas ---
    for clave, resp in respuestas.items():
        if clave in texto:
            recordar(f"Ryki: {resp}")
            return {"reply": resp}

    # --- Contexto de conversación ---
    if any(p in texto for p in ["eso", "anterior", "también", "sirve", "funciona", "lo de"]):
        tema = obtener_tema_anterior()
        if tema:
            resultado = buscar_wikipedia(f"{tema} {texto}") or buscar_duckduckgo(f"{tema} {texto}")
            if resultado:
                respuesta = f"Sobre lo que se mencionó antes ('{tema}'): {resultado}"
                recordar(f"Ryki: {respuesta}")
                return {"reply": respuesta}

    # --- Buscar información general ---
    resultado = buscar_wikipedia(texto) or buscar_duckduckgo(texto)
    if resultado:
        recordar(f"Ryki: {resultado}")
        return {"reply": resultado}

    # --- Si no encuentra nada ---
    respuesta = "No estoy seguro sobre eso , pero puedo seguir aprendiendo de lo que me digan los usuarios."
    recordar(f"Ryki: {respuesta}")
    return {"reply": respuesta}
