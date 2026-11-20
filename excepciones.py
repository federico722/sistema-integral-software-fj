# Archivo: excepciones.py

class ErrorSistema(Exception):
    """Base de todas las excepciones del sistema."""

class ErrorValidacion(ErrorSistema):
    """Excepción base para errores de validación."""
    pass

class ErrorTipo(ErrorValidacion):
    pass

class ErrorFormato(ErrorValidacion):
    pass

class ClienteNoEncontrado(ErrorSistema):
    pass

class ServicioNoEncontrado(ErrorSistema):
    pass

# Nuevas excepciones para Reservas
class ReservaInvalida(Exception):
    """Se lanza cuando los datos de la reserva no son válidos."""
    pass

class ServicioNoDisponible(ErrorSistema):
    """Se lanza cuando el servicio está inactivo o no disponible."""
    pass

class OperacionNoPermitida(Exception):
    """Se lanza cuando se intenta hacer algo no permitido (ej. cancelar lo ya cancelado)."""
    pass

class FechaIncompatible(ErrorSistema):
    pass