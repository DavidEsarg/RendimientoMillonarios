from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import sqlite3
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo para los datos del jugador
class Player(BaseModel):
    id: int
    nombre: str
    numero: int
    posicion: str
    equipo: str
    altura: float
    edad: int
    goles: int
    asistencias: int
    partidos: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    estado: str
    titular: str

# Modelo para los datos del partido
class Match(BaseModel):
    id: int
    fecha: str
    equipo_local: str
    equipo_visitante: str
    resultado: str
    estadio: str

# Inicializar la base de datos SQLite
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    # Crear tabla de jugadores si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            numero INTEGER,
            posicion TEXT,
            equipo TEXT,
            altura REAL,
            edad INTEGER,
            goles INTEGER,
            asistencias INTEGER,
            partidos INTEGER,
            tarjetas_amarillas INTEGER,
            tarjetas_rojas INTEGER,
            estado TEXT,
            titular TEXT
        )
    ''')
    # Crear tabla de partidos si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            equipo_local TEXT,
            equipo_visitante TEXT,
            resultado TEXT,
            estadio TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada exitosamente.")

# Ejecutar inicialización al inicio
init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Template index.html not found")

@app.get("/plantilla", response_class=HTMLResponse)
async def plantilla():
    try:
        with open("templates/plantilla.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Template plantilla.html not found")

@app.get("/partidos", response_class=HTMLResponse)
async def partidos():
    try:
        with open("templates/partidos.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Template partidos.html not found")

@app.get("/rendimiento", response_class=HTMLResponse)
async def rendimiento():
    try:
        with open("templates/rendimiento.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Template rendimiento.html not found")

@app.get("/players", response_class=HTMLResponse)
async def get_players():
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM players")
        players = c.fetchall()
        conn.close()
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer jugadores: {str(e)}")

@app.post("/save-player")
async def save_player(player: Player):
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO players (id, nombre, numero, posicion, equipo, altura, edad, goles, asistencias, partidos, tarjetas_amarillas, tarjetas_rojas, estado, titular)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player.id, player.nombre, player.numero, player.posicion, player.equipo,
            player.altura, player.edad, player.goles, player.asistencias, player.partidos,
            player.tarjetas_amarillas, player.tarjetas_rojas, player.estado, player.titular
        ))
        conn.commit()
        conn.close()
        return {"message": "Jugador guardado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar jugador: {str(e)}")

@app.get("/matches", response_class=HTMLResponse)
async def get_matches():
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM matches")
        matches = c.fetchall()
        conn.close()
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer partidos: {str(e)}")

@app.post("/save-match")
async def save_match(match: Match):
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO matches (id, fecha, equipo_local, equipo_visitante, resultado, estadio)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            match.id, match.fecha, match.equipo_local, match.equipo_visitante,
            match.resultado, match.estadio
        ))
        conn.commit()
        conn.close()
        return {"message": "Partido guardado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar partido: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)