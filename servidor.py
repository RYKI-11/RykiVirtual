from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import wikipedia
from duckduckgo_search import DDGS

app = FastAPI()

# Permitir peticiones desde cualquier origen (para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "Servidor activo"}

@app.get("/buscar")
def buscar(query: str):
    resultados = []

    # --- Buscar en Wikipedia ---
    try:
        wikipedia.set_lang("es")
        resumen = wikipedia.summary(query, sentences=2)
        resultados.append({
            "fuente": "Wikipedia",
            "titulo": query.title(),
            "contenido": resumen,
            "url": f"https://es.wikipedia.org/wiki/{query.replace(' ', '_')}"
        })
    except Exception:
        resultados.append({
            "fuente": "Wikipedia",
            "titulo": "Sin resultados",
            "contenido": "No se encontró información en Wikipedia.",
            "url": None
        })

    # --- Buscar en DuckDuckGo ---
    try:
        with DDGS() as ddgs:
            resultados_ddg = ddgs.text(query, region='es-es', safesearch='Moderate', max_results=3)
            for r in resultados_ddg:
                resultados.append({
                    "fuente": "DuckDuckGo",
                    "titulo": r.get("title"),
                    "contenido": r.get("body"),
                    "url": r.get("href")
                })
    except Exception:
        resultados.append({
            "fuente": "DuckDuckGo",
            "titulo": "Error",
            "contenido": "No se pudo conectar con DuckDuckGo.",
            "url": None
        })

    return {"resultados": resultados}
