# Archivo: reserva.py
from datetime import datetime, timedelta
from entidad_sistema import EntidadSistema
from cliente import Cliente
from servicio import Servicio
from logs import registrar_en_log
from excepciones import (ErrorSistema, ReservaInvalida, ServicioNoDisponible,
                         OperacionNoPermitida, FechaIncompatible)

class Reserva:
    def __init__(self, cliente, servicio, fecha, hora_inicio, duracion_horas):
        # Validamos los datos antes de guardar
        self.validar_datos(cliente, servicio, fecha, hora_inicio, duracion_horas)
        inicio = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M")
        self.__cliente = cliente
        self.__servicio = servicio
        self.__fecha = fecha
        self.__hora_inicio = hora_inicio
        self.__duracion_horas = duracion_horas
        self.__inicio = inicio
        self.__fin = inicio + timedelta(hours=duracion_horas)
        self.__estado = "Pendiente"   # Pendiente, Confirmada, Cancelada, Finalizada
        self.__costo_total = 0.0

      # ---------- getters ----------
    def getCliente(self): return self.__cliente
    def getServicio(self): return self.__servicio
    def getEstado(self): return self.__estado
    def getCostoTotal(self): return self.__costo_total
    def getInicio(self): return self.__inicio
    def getFin(self): return self.__fin

    def getInformacion(self):
        return [self.getIdEntidad(), self.__cliente.getNombre(), self.__servicio.getNombre(),
                self.__fecha, self.__hora_inicio, self.__fin.strftime("%H:%M"),
                self.__duracion_horas, self.__costo_total, self.__estado]

    # ---------- validacion ----------  
    def validar_datos(self, cliente, servicio, fecha, hora_inicio, duracion):
        """Valida los datos usando try/except/else/finally"""
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalida("Se necesita un cliente valido.")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalida("Se necesita un servicio valido.")
            if not servicio.puedeReservarse():
                raise ServicioNoDisponible(f"El servicio {servicio.getNombre()} no esta disponible.")
            if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
                raise ReservaInvalida("La duracion debe ser un numero mayor a 0 horas.")
            if not fecha or not hora_inicio:
                raise ReservaInvalida("La fecha y la hora son obligatorias.")
            try:
                inicio = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M")
            except ValueError as e:
                raise FechaIncompatible(
                    "Fecha u hora invalida (use AAAA-MM-DD y HH:MM).") from e
            if (inicio + timedelta(hours=duracion)).date() != inicio.date():
                raise FechaIncompatible("La reserva debe terminar el mismo dia en que empieza.")
        except ErrorSistema as e:
            # error propio: solo se registra y se deja pasar con su tipo original
            registrar_en_log(f"Fallo al crear reserva: {e}")
            raise
        except Exception as e:
            # error inesperado de Python: se encadena como ReservaInvalida
            registrar_en_log(f"Fallo inesperado al crear reserva: {e}")
            raise ReservaInvalida(f"Error al crear la reserva: {e}") from e
        else:
            print("Validacion de reserva exitosa.")
        finally:
            print("--- Fin de la validacion de la reserva ---")

     # ---------- costo ----------
    def calcularCosto(self, impuesto=0.0, descuento=0.0, **opciones):
        # opciones permite pasar datos propios de un servicio, ej: unidades=2 para Equipo
        return self.__servicio.calcularCosto(self.__duracion_horas, impuesto, descuento, **opciones)

    # ---------- operaciones ----------
    def confirmarReserva(self, impuesto=0.0, descuento=0.0, **opciones):
        try:
            if self.__estado != "Pendiente":
                raise OperacionNoPermitida(
                    f"No se puede confirmar una reserva en estado {self.__estado}.")
            # primero calculamos: si falla, el estado queda intacto
            costo = self.calcularCosto(impuesto, descuento, **opciones)
            self.__costo_total = costo
            self.__estado = "Confirmada"
        except ErrorSistema as e:
            registrar_en_log(f"ERROR al confirmar reserva {self.getIdEntidad()}: {e}")
            raise
        else:
            registrar_en_log(f"EVENTO: reserva confirmada para {self.__cliente.getNombre()} "
                             f"({self.__servicio.getNombre()}, {self.__duracion_horas} h, ${costo}).")
            return costo
    # cancelar reserva 
    def cancelarReserva(self):
        try:
            # reserva cancelada, si el estado de la reserva es Cancelado, entonces es una operacion no permitida
            if self.__estado == "Cancelada":
                raise OperacionNoPermitida("La reserva ya esta cancelada.")
            # reserva finalizada, si el estado de la reserva es finalizada, entonces es una operacion no permitida, porque no se cancela una reserva finalizada
            if self.__estado == "Finalizada":
                raise OperacionNoPermitida("No se puede cancelar una reserva finalizada.")
            # el estado de la reserva se actualiza, ha cancelada
            self.__estado = "Cancelada"
        except OperacionNoPermitida as e:
            # registra los errores al cancelar reservas
            registrar_en_log(f"ERROR al cancelar reserva {self.getIdEntidad()}: {e}")
            raise
        else:
            # registra un evento donde la reserva si es cancelada correctamente
            registrar_en_log(f"EVENTO: reserva cancelada para {self.__cliente.getNombre()}.")

    # procesamos el estado de las reservas
    def procesarReserva(self):
        try:
            # si la reserva no esta confirmada, entonces es una operacion no permitida
            if self.__estado != "Confirmada":
                raise OperacionNoPermitida("Solo se puede procesar una reserva confirmada.")
            # entonces cambia el estado de la reserva a finalizada, dado que no esta confirmada entonces esta finalizada
            self.__estado = "Finalizada"
        except OperacionNoPermitida as e:
            # regitra los errores al procesar la reserva
            registrar_en_log(f"ERROR al procesar reserva {self.getIdEntidad()}: {e}")
            raise 
        else:
            registrar_en_log(f"EVENTO: reserva finalizada de {self.__cliente.getNombre()}.")

     # ---------- disponibilidad ----------
    def seSolapaCon(self, otra):
        """True si los intervalos de tiempo de las dos reservas se cruzan."""
        # el inicio de esta reserva ocurre antes de que termine la otra reserva, 
        # el inicio de la otra reserva ocurre antes de que termine esta reserva.
        # piensen que estamos calculando una pregunta de si o no, comparando cuatro numeros
        # en una sola operacion
        return self.__inicio < otra.getFin() and otra.getInicio() < self.__fin

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