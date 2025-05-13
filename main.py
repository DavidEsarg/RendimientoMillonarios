from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Jugador, JugadorConId, Partido, PartidoConId, TorneoStats
from operations import leer_todos_los_jugadores, leer_todos_los_partidos, escribir_jugadores, escribir_partidos
from database import get_db

app = FastAPI()


@app.get("/allplayers", response_model=List[JugadorConId])
async def obtener_todos_los_jugadores(db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    jugadores_filtrados = [jugador for jugador in jugadores if jugador.estado == "activo" and jugador.eliminado == "no"]
    if not jugadores_filtrados:
        raise HTTPException(status_code=404, detail="No hay jugadores activos")
    return jugadores_filtrados


@app.get("/players/search", response_model=List[JugadorConId])
async def buscar_jugadores(apellido: Optional[str] = None, posicion: Optional[str] = None,
                           numero_camiseta: Optional[int] = None, db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    jugadores_filtrados = [
        jugador for jugador in jugadores
        if (apellido is None or apellido.lower() in jugador.nombre.lower()) and
           (posicion is None or posicion.lower() == jugador.posicion.lower()) and
           (numero_camiseta is None or numero_camiseta == jugador.numero) and
           (jugador.estado == "activo" and jugador.eliminado == "no")
    ]
    if not jugadores_filtrados:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores")
    return jugadores_filtrados


@app.post("/player", response_model=JugadorConId)
async def agregar_jugador(jugador: Jugador, db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    nuevo_id = max([j.id for j in jugadores], default=0) + 1
    datos_jugador = jugador.dict()
    datos_jugador["id"] = nuevo_id
    jugador_con_id = JugadorConId(**datos_jugador)
    jugadores.append(jugador_con_id)
    escribir_jugadores(db, jugadores)
    return jugador_con_id


@app.put("/player/{id_jugador}", response_model=JugadorConId)
async def modificar_jugador(id_jugador: int, jugador_actualizado: Jugador, db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    for i, jugador in enumerate(jugadores):
        if jugador.id == id_jugador:
            datos_jugador = jugador_actualizado.dict()
            datos_jugador["id"] = id_jugador
            jugadores[i] = JugadorConId(**datos_jugador)
            escribir_jugadores(db, jugadores)
            return jugadores[i]
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


@app.delete("/player/{id_jugador}")
async def eliminar_jugador(id_jugador: int, db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    for i, jugador in enumerate(jugadores):
        if jugador.id == id_jugador:
            jugadores[i].eliminado = "sí"
            escribir_jugadores(db, jugadores)
            return {"message": "Jugador eliminado"}
    raise HTTPException(status_code=404, detail="Jugador no encontrado")


@app.get("/deletedplayers", response_model=List[JugadorConId])
async def obtener_jugadores_eliminados(db: Session = Depends(get_db)):
    jugadores = leer_todos_los_jugadores(db)
    jugadores_eliminados = [jugador for jugador in jugadores if jugador.eliminado == "sí"]
    if not jugadores_eliminados:
        raise HTTPException(status_code=404, detail="No hay jugadores eliminados")
    return jugadores_eliminados


@app.get("/allgames", response_model=List[PartidoConId])
async def obtener_todos_los_partidos(db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    print(f"Partidos antes de filtrar: {partidos}")
    partidos_filtrados = [partido for partido in partidos if partido.estado == "jugado" and partido.eliminado == "no"]
    print(f"Partidos después de filtrar: {partidos_filtrados}")
    if not partidos_filtrados:
        raise HTTPException(status_code=404, detail="No hay partidos")
    return partidos_filtrados


@app.get("/games/search", response_model=List[PartidoConId])
async def buscar_partidos(torneo: Optional[str] = None, rival: Optional[str] = None, db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    partidos_filtrados = [
        partido for partido in partidos
        if (torneo is None or torneo.lower() in partido.torneo.lower()) and
           (rival is None or rival.lower() in partido.rival.lower()) and
           (partido.estado == "jugado" and partido.eliminado == "no")
    ]
    if not partidos_filtrados:
        raise HTTPException(status_code=404, detail="No se encontraron partidos")
    return partidos_filtrados


@app.post("/game", response_model=PartidoConId)
async def agregar_partido(partido: Partido, db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    nuevo_id = max([p.id_partido for p in partidos], default=0) + 1
    datos_partido = partido.dict()
    datos_partido["id_partido"] = nuevo_id
    partido_con_id = PartidoConId(**datos_partido)
    partidos.append(partido_con_id)
    escribir_partidos(db, partidos)
    return partido_con_id


@app.put("/game/{id_partido}", response_model=PartidoConId)
async def modificar_partido(id_partido: int, partido_actualizado: Partido, db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    for i, partido in enumerate(partidos):
        if partido.id_partido == id_partido:
            datos_partido = partido_actualizado.dict()
            datos_partido["id_partido"] = id_partido
            partidos[i] = PartidoConId(**datos_partido)
            escribir_partidos(db, partidos)
            return partidos[i]
    raise HTTPException(status_code=404, detail="Partido no encontrado")


@app.delete("/game/{id_partido}")
async def eliminar_partido(id_partido: int, db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    for i, partido in enumerate(partidos):
        if partido.id_partido == id_partido:
            partidos[i].eliminado = "sí"
            escribir_partidos(db, partidos)
            return {"message": "Partido eliminado"}
    raise HTTPException(status_code=404, detail="Partido no encontrado")


@app.get("/deletedgames", response_model=List[PartidoConId])
async def obtener_partidos_eliminados(db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    partidos_eliminados = [partido for partido in partidos if partido.eliminado == "sí"]
    if not partidos_eliminados:
        raise HTTPException(status_code=404, detail="No hay partidos eliminados")
    return partidos_eliminados


@app.get("/stats/comparisons", response_model=List[TorneoStats])
async def comparar_estadisticas_torneos(db: Session = Depends(get_db)):
    partidos = leer_todos_los_partidos(db)
    partidos_filtrados = [partido for partido in partidos if partido.estado == "jugado" and partido.eliminado == "no"]

    torneos = [
        {"nombre": "Torneo Apertura 2024", "torneo": "Torneo Apertura", "año": "2024"},
        {"nombre": "Torneo Finalización 2024", "torneo": "Torneo Finalización", "año": "2024"},
        {"nombre": "Torneo Apertura 2025", "torneo": "Torneo Apertura", "año": "2025"}
    ]

    resultados = []

    for torneo in torneos:
        partidos_torneo = [
            p for p in partidos_filtrados
            if p.torneo == torneo["torneo"] and p.fecha.startswith(torneo["año"])
        ]
        ganados = sum(1 for p in partidos_torneo if p.goles_millonarios > p.goles_rival)
        perdidos = sum(1 for p in partidos_torneo if p.goles_millonarios < p.goles_rival)
        empatados = sum(1 for p in partidos_torneo if p.goles_millonarios == p.goles_rival)
        total_partidos = len(partidos_torneo)
        stats = TorneoStats(
            torneo=torneo["nombre"],
            ganados=ganados,
            perdidos=perdidos,
            empatados=empatados,
            total_partidos=total_partidos
        )
        resultados.append(stats)

    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron datos para los torneos especificados")

    return resultados