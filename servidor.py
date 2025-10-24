from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os 

app = FastAPI()

# servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# servir página principal
@app.get("/")
async def home():
    return FileResponse("index.html")



# --- FUNCIONES DE MEMORIA ---

MEMORIA_FILE = "memoria.json"

def cargar_memoria():
    if not os.path.exists(MEMORIA_FILE):
        return {}
    with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {} 
        
        def guaradar_memoria(data):
            with open(MEMORIA_FILE, "W", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


# --- ENDPOINT PRINCIPAL DEL CHAT ---

@app.post ("/chat")
async def chat(request: Request):
    data = await request.json()
    mensaje_usuario = data.get("mensaje", "").strip()
    memoria = cargar_memoria()

    # Recuperar contexto anterior (si existe)
    historial = memoria.get("historial", [])

    # Guardar nuevo mensaje en el historial
    historial.append({"rol": "usuario", "contenido": mensaje_usuario})

    # Aquí pondríamos la lógica de IA (de momento, una respuesta simulada)
    respuesta = generar_respuesta(mensaje_usuario, historial)
    
    # Guardar la respuesta en la memoria
    historial.append({"rol": "bot", "contenido": respuesta})