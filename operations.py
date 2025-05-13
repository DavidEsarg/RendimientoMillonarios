from typing import List
from models import JugadorConId, PartidoConId
from db_models import Player, Game

def leer_todos_los_jugadores(db) -> List[JugadorConId]:
    jugadores_db = db.query(Player).filter(Player.estado == "activo", Player.eliminado == "no").all()
    return [
        JugadorConId(
            id=jugador.id,
            nombre=jugador.nombre,
            numero=jugador.numero,
            posicion=jugador.posicion,
            equipo=jugador.equipo,
            altura=jugador.altura,
            edad=jugador.edad,
            goles=jugador.goles,
            asistencias=jugador.asistencias,
            partidos_jugados=jugador.partidos_jugados,
            tarjetas_amarillas=jugador.tarjetas_amarillas,
            tarjetas_rojas=jugador.tarjetas_rojas,
            estado=jugador.estado,
            eliminado=jugador.eliminado
        )
        for jugador in jugadores_db
    ]

def eliminar_jugador(id_jugador: int, db) -> str:
    jugador = db.query(Player).filter(Player.id == id_jugador).first()
    if not jugador:
        return None
    jugador.eliminado = "sí"
    db.commit()
    return "Jugador eliminado"

def leer_todos_los_partidos(db) -> List[PartidoConId]:
    partidos_db = db.query(Game).filter(Game.estado == "jugado", Game.eliminado == "no").all()
    return [
        PartidoConId(
            id_partido=partido.id_partido,
            fecha=partido.fecha,
            torneo=partido.torneo,
            rival=partido.rival,
            goles_millonarios=partido.goles_millonarios,
            goles_rival=partido.goles_rival,
            jugador_destacado=partido.jugador_destacado,
            goles=partido.goles,
            asistencias=partido.asistencias,
            tarjetas_amarillas=partido.tarjetas_amarillas,
            tarjetas_rojas=partido.tarjetas_rojas,
            posesion=partido.posesion,
            estado=partido.estado,
            eliminado=partido.eliminado
        )
        for partido in partidos_db
    ]

def eliminar_partido(id_partido: int, db) -> str:
    partido = db.query(Game).filter(Game.id_partido == id_partido).first()
    if not partido:
        return None
    partido.eliminado = "sí"
    db.commit()
    return "Partido eliminado"

def leer_jugadores_eliminados(db) -> List[JugadorConId]:
    jugadores_db = db.query(Player).filter(Player.eliminado == "sí").all()
    return [
        JugadorConId(
            id=jugador.id,
            nombre=jugador.nombre,
            numero=jugador.numero,
            posicion=jugador.posicion,
            equipo=jugador.equipo,
            altura=jugador.altura,
            edad=jugador.edad,
            goles=jugador.goles,
            asistencias=jugador.asistencias,
            partidos_jugados=jugador.partidos_jugados,
            tarjetas_amarillas=jugador.tarjetas_amarillas,
            tarjetas_rojas=jugador.tarjetas_rojas,
            estado=jugador.estado,
            eliminado=jugador.eliminado
        )
        for jugador in jugadores_db
    ]

def leer_partidos_eliminados(db) -> List[PartidoConId]:
    partidos_db = db.query(Game).filter(Game.eliminado == "sí").all()
    return [
        PartidoConId(
            id_partido=partido.id_partido,
            fecha=partido.fecha,
            torneo=partido.torneo,
            rival=partido.rival,
            goles_millonarios=partido.goles_millonarios,
            goles_rival=partido.goles_rival,
            jugador_destacado=partido.jugador_destacado,
            goles=partido.goles,
            asistencias=partido.asistencias,
            tarjetas_amarillas=partido.tarjetas_amarillas,
            tarjetas_rojas=partido.tarjetas_rojas,
            posesion=partido.posesion,
            estado=partido.estado,
            eliminado=partido.eliminado
        )
        for partido in partidos_db
    ]