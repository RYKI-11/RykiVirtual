from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import wikipedia
from ddgs import DDGS
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")

# --------- BASE DE DATOS ---------
con=sqlite3.connect("memory.db",check_same_thread=False)
cur=con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS chat(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
bot TEXT
)
""")
con.commit()

def save(u,b):
    cur.execute("INSERT INTO chat VALUES(NULL,?,?)",(u,b))
    con.commit()

def load():
    cur.execute("SELECT user,bot FROM chat")
    return cur.fetchall()

# --------- CHAT ---------

class Chat(BaseModel):
    message:str

def wiki(q):
    try:
        wikipedia.set_lang("es")
        return wikipedia.summary(q,2)
    except:
        return None

def ddg(q):
    try:
        with DDGS() as d:
            r=list(d.text(q,max_results=1))
            return r[0]["body"] if r else None
    except:
        return None

@app.post("/chat")
def chat(data:Chat):

    q=data.message.lower()

    base={
    "hola":"Hola soy Ryki ",
    "como estas":"Muy bien ",
    "quien eres":"Soy Ryki Virtual",
    "adios":"Hasta luego "
    }

    if q in base:
        r=base[q]
    else:
        r=wiki(q)
        if not r:
            r=ddg(q)
        if not r:
            r="No encontré información "

    save(q,r)
    return {"reply":r}

@app.get("/memory")
def memory():
    return load()

@app.get("/clear")
def clear():
    cur.execute("DELETE FROM chat")
    con.commit()
    return {"ok":True}
