from pydantic import BaseModel

class JugadorConId(BaseModel):
    id: int
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
    estado: str
    eliminado: str

    class Config:
        from_attributes = True

class PartidoConId(BaseModel):
    id_partido: int
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
    estado: str
    eliminado: str

    class Config:
        from_attributes = True