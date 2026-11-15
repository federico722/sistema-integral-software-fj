# Archivo: reserva.py
from logs import registrar_en_log
from excepciones import ReservaInvalida, ServicioNoDisponible, OperacionNoPermitida

class Reserva:
    def __init__(self, cliente, servicio, fecha, hora_inicio, duracion_horas):
        # Validamos los datos antes de guardar
        self.validar_datos(cliente, servicio, fecha, hora_inicio, duracion_horas)
        
        self.cliente = cliente
        self.servicio = servicio
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.duracion_horas = duracion_horas
        self.estado = "Pendiente" # Estados: Pendiente, Confirmada, Cancelada
        self.costo_total = 0.0

    def validar_datos(self, cliente, servicio, fecha, hora_inicio, duracion):
        """Valida que los datos de la reserva sean correctos usando try/except/else/finally"""
        try:
            if cliente is None:
                raise ReservaInvalida("El cliente no puede estar vacio.")
            if servicio is None:
                raise ReservaInvalida("El servicio no puede estar vacio.")
            if not servicio.get("disponible", False):
                raise ServicioNoDisponible(f"El servicio {servicio.get('nombre')} no esta disponible.")
            if duracion <= 0:
                raise ReservaInvalida("La duración debe ser mayor a 0 horas.")
            if not fecha or not hora_inicio:
                raise ReservaInvalida("La fecha y la hora son obligatorias.")
                
        except Exception as e:
            # 1. Registramos el error en el log
            registrar_en_log(f"Fallo al crear reserva: {str(e)}")
            # 2. Lanzamos el error (encadenamiento)
            raise ReservaInvalida(f"Error al crear la reserva: {e}") from e
        else:
            # Esto se ejecuta si NO hubo errores
            print("Validacion de reserva exitosa.")
        finally:
            # Esto se ejecuta SIEMPRE, haya error o no
            print("--- Fin de la validacion de la reserva ---")

    def confirmar_reserva(self):
        """Cambia el estado a Confirmada, con manejo de excepciones"""
    try:
            if self.estado == "Cancelada":
                raise OperacionNoPermitida("No se puede confirmar una reserva que ya fue cancelada.")
            
            self.estado = "Confirmada"
            # Simulamos el cálculo del costo (ej: 50.000 por hora)
            self.costo_total = self.duracion_horas * 50000
            print(f"Reserva confirmada. Costo total: ${self.costo_total}")
            
            # Aquí está la línea del log corregida y sin símbolos raros
            registrar_en_log(f"EVENTO: Reserva confirmada para {self.cliente} por {self.duracion_horas} horas.")
            
    except OperacionNoPermitida as e:
            registrar_en_log(f"ERROR: {str(e)}")
            print(f"Error: {e}")

    def cancelar_reserva(self):
        """Cancela la reserva"""
        try:
            if self.estado == "Cancelada":
                raise OperacionNoPermitida("La reserva ya esta cancelada.")
            
            self.estado = "Cancelada"
            print(f"Reserva cancelada exitosamente.")
            registrar_en_log(f"Reserva cancelada para {self.cliente}.")
            
        except OperacionNoPermitida as e:
            registrar_en_log(str(e))
            print(f"Error: {e}")

# ==========================================
# PRUEBAS PARA VER QUE FUNCIONA (Simulacion)
# ==========================================
if __name__ == "__main__":
    print("\n--- PRUEBA 1: Reserva Exitosa ---")
    # Simulamos un servicio (ya que no tenemos la clase aun)
    servicio_sala = {"nombre": "Sala de Juntas", "disponible": True}
    
    try:
        # Creamos la reserva
        reserva1 = Reserva(cliente="Federico", servicio=servicio_sala, fecha="2026-11-20", hora_inicio="10:00", duracion_horas=2)
        # Confirmamos
        reserva1.confirmar_reserva()
    except Exception as e:
        print(f"El programa no se detuvo. Error controlado: {e}")

    print("\n--- PRUEBA 2: Reserva Fallida (Servicio no disponible) ---")
    servicio_equipo = {"nombre": "Computador", "disponible": False} # Falso para que falle
    
    try:
        reserva2 = Reserva(cliente="Federico", servicio=servicio_equipo, fecha="2026-11-21", hora_inicio="14:00", duracion_horas=3)
    except Exception as e:
        # Aqui el programa atrapa el error y NO se cae
        print(f"El programa no se detuvo. Error controlado: {e}")