from fastapi import FastAPI, Depends, HTTPException
from typing import List
from models import JugadorConId, PartidoConId
from database import get_db, Base, engine
from operations import leer_todos_los_jugadores, eliminar_jugador, leer_todos_los_partidos, eliminar_partido, leer_jugadores_eliminados, leer_partidos_eliminados
from sqlalchemy.orm import Session

# Crear las tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/allplayers", response_model=List[JugadorConId])
async def obtener_todos_los_jugadores(db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No hay jugadores activos")
    return jugadores

@app.delete("/player/{id_jugador}")
async def eliminar_jugador_endpoint(id_jugador: int, db: Session = Depends(get_db)):
    mensaje = eliminar_jugador(id_jugador, db)
    if not mensaje:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador eliminado"}

@app.get("/allgames", response_model=List[PartidoConId])
async def obtener_todos_los_partidos(db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    if not partidos:
        raise HTTPException(status_code=404, detail="No hay partidos")
    return partidos

@app.delete("/game/{id_partido}")
async def eliminar_partido_endpoint(id_partido: int, db: Session = Depends(get_db)):
    mensaje = eliminar_partido(id_partido, db)
    if not mensaje:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return {"message": "Partido eliminado"}

@app.get("/deletedplayers", response_model=List[JugadorConId])
async def obtener_jugadores_eliminados(db: Session = Depends(get_db)):
    jugadores = leer_jugadores_eliminados(db)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No hay jugadores eliminados")
    return jugadores

@app.get("/deletedgames", response_model=List[PartidoConId])
async def obtener_partidos_eliminados(db: Session = Depends(get_db)):
    partidos = leer_partidos_eliminados(db)
    if not partidos:
        raise HTTPException(status_code=404, detail="No hay partidos eliminados")
    return partidos