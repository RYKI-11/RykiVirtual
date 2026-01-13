from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/chat")
def chat(message: str = Form(...)):
    return JSONResponse({"response": f"Has dicho: {message}"})
