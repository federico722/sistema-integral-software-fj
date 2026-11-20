
from fase4 import Servicio
from logs import registrar_en_log
from excepciones import ErrorValidacion, ErrorTipo, ServicioNoEncontrado

class SistemaGestionServicio:

    def __init__(self):
        self.__servicios = []
    # registrar servicios 
    def registrarServicio(self, servicio):
        try:
            if self.verificarServicioExistente(servicio.getNombre()):
                registrar_en_log(f"Intento de registrar servicio duplicado: {servicio.getNombre()}")
                raise ErrorValidacion("Ya existe un servicio con ese nombre.")
            if not isinstance(servicio, Servicio):
                raise ErrorTipo("El objeto debe ser un servicio válido.")

            identificacion = servicio.getIdEntidad()

            for existente in self.__servicios:
                if existente.getIdEntidad() == identificacion:
                    raise ValueError("El servicio ya se encuentra registrado.")

            self.__servicios.append(servicio)
            return servicio

        except Exception as e:
            registrar_en_log(f"Error al registrar servicio: {e}")
            raise

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
