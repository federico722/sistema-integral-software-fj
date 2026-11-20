# Archivo: logs.py
import datetime
import os

# ruta fija junto a este archivo: el log siempre queda en el mismo lugar
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "errores.log")


def registrar_en_log(mensaje_error):
    """Guarda un mensaje en el archivo errores.log"""
    try:
        with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha_hora}] {mensaje_error}\n")
    except Exception as e:
        print(f"No se pudo guardar en el log: {e}")


def leer_log():
    """Devuelve el contenido del log, o cadena vacia si aun no existe."""
    try:
        with open(RUTA_LOG, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return ""