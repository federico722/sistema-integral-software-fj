# Archivo: logs.py
import datetime # Para saber la fecha y hora del error

def registrar_en_log(mensaje_error):
    """Guarda un mensaje de error en el archivo errores.log"""
    try:
        # Abrimos el archivo en modo 'a' (append = añadir al final)
        with open("errores.log", "a", encoding="utf-8") as archivo:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha_hora}] {mensaje_error}\n")
    except Exception as e:
        # Si falla el guardado, al menos lo mostramos en consola
        print(f"No se pudo guardar en el log: {e}")