from pydantic import BaseModel

class Jugador(BaseModel):
    id:int
    nombre: str
    numero: int
    posicion: str
    equipo: str
    altura: float
    edad: int
    goles: int
    asistencias: int
    partidos_jugados: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    estado: str = "activo"
    eliminado: str = "no"

class JugadorConId(Jugador):
    id: int

class Partido(BaseModel):
    fecha: str
    torneo: str
    rival: str
    goles_millonarios: int
    goles_rival: int
    jugador_destacado: str
    goles: int
    asistencias: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    posesion: float
    estado: str = "jugado"
    eliminado: str = "no"

class PartidoConId(Partido):
    id_partido: int

class TorneoStats(BaseModel):
    torneo: str
    ganados: int
    perdidos: int
    empatados: int
    total_partidos: int