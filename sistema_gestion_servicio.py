
from fase4 import Servicio
from logs import registrar_en_log
from excepciones import ErrorValidacion, ErrorTipo, ServicioNoEncontrado

class SistemaGestionServicio:

    def __init__(self):
        self.__servicios = []
    # registrar servicios 
    def registrarServicio(self, servicio):
        # primero el tipo: si no es un Servicio, no se le puede pedir getNombre()
        if not isinstance(servicio, Servicio):
            registrar_en_log("Se intento registrar un objeto que no es un servicio.")
            raise ErrorTipo("El objeto debe ser un servicio válido.")
        # los servicios se identifican por nombre, asi que no puede haber dos iguales
        if self.verificarServicioExistente(servicio.getNombre()):
            registrar_en_log(f"Intento de registrar servicio duplicado: {servicio.getNombre()}")
            raise ErrorValidacion("Ya existe un servicio con ese nombre.")
        self.__servicios.append(servicio)
        registrar_en_log(f"EVENTO: servicio registrado: {servicio.getNombre()}.")
        return servicio

    def buscarServicio(self, identificacion):
        try:
            for servicio in self.__servicios:
                if (str(servicio.getIdEntidad()) == str(identificacion)
                        or servicio.getNombre().lower()
                        == str(identificacion).lower()):
                    return servicio

            return None

        except Exception as e:
            registrar_en_log(f"Error al buscar servicio: {e}")
            raise

    def listarServicios(self):
        return self.__servicios.copy()

    def listarServiciosDisponibles(self):
        return [
            servicio for servicio in self.__servicios
            if servicio.puedeReservarse()
        ]

    def eliminarServicio(self, identificacion):
        try:
            servicio = self.buscarServicio(identificacion)

            if servicio is None:
                raise ServicioNoEncontrado("No se encontró el servicio solicitado.")

            self.__servicios.remove(servicio)
            registrar_en_log(f"EVENTO: servicio eliminado: {servicio.getNombre()}.")
            return True

        except Exception as e:
            registrar_en_log(f"Error al eliminar servicio: {e}")
            raise

    def cantidadServicios(self):
        return len(self.__servicios)

    def obtenerInformacionServicios(self):
        return [
            servicio.getInformacion()
            for servicio in self.__servicios
        ]
    
    # verificar si el servicio esta disponible
    def verificarServicioExistente(self, identificacion):
        return self.buscarServicio(identificacion) is not None