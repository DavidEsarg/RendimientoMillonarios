from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    posicion = Column(String, nullable=False)
    equipo = Column(String, nullable=False)
    altura = Column(Float, nullable=False)
    edad = Column(Integer, nullable=False)
    goles = Column(Integer, nullable=False)
    asistencias = Column(Integer, nullable=False)
    partidos_jugados = Column(Integer, nullable=False)
    tarjetas_amarillas = Column(Integer, nullable=False)
    tarjetas_rojas = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="activo")
    eliminado = Column(String, nullable=False, default="no")

class Game(Base):
    __tablename__ = "games"

    id_partido = Column(Integer, primary_key=True, index=True)
    fecha = Column(String, nullable=False)
    torneo = Column(String, nullable=False)
    rival = Column(String, nullable=False)
    goles_millonarios = Column(Integer, nullable=False)
    goles_rival = Column(Integer, nullable=False)
    jugador_destacado = Column(String, nullable=False)
    goles = Column(Integer, nullable=False)
    asistencias = Column(Integer, nullable=False)
    tarjetas_amarillas = Column(Integer, nullable=False)
    tarjetas_rojas = Column(Integer, nullable=False)
    posesion = Column(Float, nullable=False)
    estado = Column(String, nullable=False, default="jugado")
    eliminado = Column(String, nullable=False, default="no")