# Archivo: sistemaGestionReserva.py
from reserva import Reserva
from logs import registrar_en_log
from excepciones import (ReservaInvalida, ReservaNoEncontrada,
                         ErrorValidacion, FechaIncompatible)

# estados en los que una reserva "ocupa" el servicio
ESTADOS_ACTIVOS = ("Pendiente", "Confirmada")

class SistemaGestionReserva:
    def __init__(self):
        self.__reservas = []

    # registrar reservas
    def registrarReserva(self, reserva):
        if not isinstance(reserva, Reserva):
            registrar_en_log("Se intento registrar un objeto que no es una reserva.")
            raise ReservaInvalida("El objeto debe ser una reserva valida.")

        # si el horario choca, verificarDisponibilidad lanza FechaIncompatible
        # y la reserva NO se agrega a la lista
        self.verificarDisponibilidad(reserva)

        self.__reservas.append(reserva)
        registrar_en_log(f"EVENTO: reserva registrada {reserva.getIdEntidad()[:8]} "
                         f"({reserva.getCliente().getNombre()} - {reserva.getServicio().getNombre()}).")

        return reserva

    def verificarDisponibilidad(self, reserva):
        """Comprueba que no exista otra reserva activa del mismo servicio en ese horario."""
        for existente in self.__reservas:
            mismo_servicio = existente.getServicio() is reserva.getServicio()
            if(mismo_servicio
                    and existente.getEstado() in ESTADOS_ACTIVOS
                    and reserva.seSolapaCon(existente)):
                registrar_en_log(
                   f"Reserva rechazada: {reserva.getServicio().getNombre()} ya esta reservado "
                   f"en ese horario (reserva {existente.getIdEntidad()[:8]}).")
                raise FechaIncompatible(
                    f"El servicio {reserva.getServicio().getNombre()} ya esta reservado en ese horario.")
            return True
        
    def buscarReserva(self, identificacion):
        """Busca por id completo o por el comienzo del id (los primeros caracteres)."""
        identificacion = str(identificacion).strip()
        if not identificacion:
            return None
        coincidencias = [r for r in self.__reservas
                         if r.getIdEntidad().startswith(identificacion)]
        if len(coincidencias) > 1:
            raise ErrorValidacion("Hay varias reservas que empiezan igual; escriba mas caracteres del id.")
        return coincidencias[0] if coincidencias else None

    def obtenerReserva(self, identificacion):
        """Como buscarReserva, pero lanza un error propio si no existe."""
        reserva = self.buscarReserva(identificacion)
        if reserva is None:
            registrar_en_log(f"Reserva no encontrada: {identificacion}")
            raise ReservaNoEncontrada("No se encontró la reserva solicitada.")
        return reserva

    def verificarReservaExistente(self, identificacion):
        return self.buscarReserva(identificacion) is not None

    def listarReservas(self):
        return self.__reservas.copy()

    def consultarHistorialCliente(self, documento):
        return [r for r in self.__reservas
                if r.getCliente().getDocumento() == documento]

    def eliminarReserva(self, identificacion):
        reserva = self.obtenerReserva(identificacion)
        self.__reservas.remove(reserva)
        registrar_en_log(f"EVENTO: reserva eliminada {reserva.getIdEntidad()[:8]}.")
        return True

    def cantidadReservas(self):
        return len(self.__reservas)

    