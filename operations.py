import csv
from typing import List
from models import JugadorConId, PartidoConId

def leer_todos_los_jugadores() -> List[JugadorConId]:
    jugadores = []
    try:
        with open("players.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    jugador = JugadorConId(**row)
                    jugador.id = int(row["id"])
                    jugador.numero = int(row["numero"])
                    jugador.altura = float(row["altura"])
                    jugador.edad = int(row["edad"])
                    jugador.goles = int(row["goles"])
                    jugador.asistencias = int(row["asistencias"])
                    jugador.partidos_jugados = int(row["partidos_jugados"])
                    jugador.tarjetas_amarillas = int(row["tarjetas_amarillas"])
                    jugador.tarjetas_rojas = int(row["tarjetas_rojas"])
                    jugadores.append(jugador)
                except (ValueError, KeyError) as e:
                    print(f"Error al procesar fila en players.csv: {row}. Error: {str(e)}")
                    continue
    except FileNotFoundError:
        print("Archivo players.csv no encontrado. Devolviendo lista vacía.")
    except PermissionError:
        print("Error de permisos al leer players.csv. Asegúrate de que el archivo no esté bloqueado.")
        raise
    except Exception as e:
        print(f"Error inesperado al leer players.csv: {str(e)}")
        raise
    return jugadores

def escribir_jugadores(jugadores: List[JugadorConId]):
    try:
        with open("players.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "id", "nombre", "numero", "posicion", "equipo", "altura", "edad",
                "goles", "asistencias", "partidos_jugados", "tarjetas_amarillas",
                "tarjetas_rojas", "estado", "eliminado"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for jugador in jugadores:
                writer.writerow(jugador.dict())
    except PermissionError:
        print("Error de permisos al escribir en players.csv. Asegúrate de que el archivo no esté bloqueado.")
        raise
    except Exception as e:
        print(f"Error inesperado al escribir en players.csv: {str(e)}")
        raise

def leer_todos_los_partidos() -> List[PartidoConId]:
    partidos = []
    try:
        with open("games.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    partido = PartidoConId(**row)
                    partido.id_partido = int(row["id_partido"])
                    partido.goles_millonarios = int(row["goles_millonarios"])
                    partido.goles_rival = int(row["goles_rival"])
                    partido.goles = int(row["goles"])
                    partido.asistencias = int(row["asistencias"])
                    partido.tarjetas_amarillas = int(row["tarjetas_amarillas"])
                    partido.tarjetas_rojas = int(row["tarjetas_rojas"])
                    partido.posesion = float(row["posesion"])
                    partidos.append(partido)
                except (ValueError, KeyError) as e:
                    print(f"Error al procesar fila en games.csv: {row}. Error: {str(e)}")
                    continue
    except FileNotFoundError:
        print("Archivo games.csv no encontrado. Devolviendo lista vacía.")
    except PermissionError:
        print("Error de permisos al leer games.csv. Asegúrate de que el archivo no esté bloqueado.")
        raise
    except Exception as e:
        print(f"Error inesperado al leer games.csv: {str(e)}")
        raise
    return partidos

def escribir_partidos(partidos: List[PartidoConId]):
    try:
        with open("games.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "id_partido", "fecha", "torneo", "rival", "goles_millonarios",
                "goles_rival", "jugador_destacado", "goles", "asistencias",
                "tarjetas_amarillas", "tarjetas_rojas", "posesion", "estado",
                "eliminado"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for partido in partidos:
                writer.writerow(partido.dict())
    except PermissionError:
        print("Error de permisos al escribir en games.csv. Asegúrate de que el archivo no esté bloqueado.")
        raise
    except Exception as e:
        print(f"Error inesperado al escribir en games.csv: {str(e)}")
        raise