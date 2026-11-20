
from servicio import Servicio
from excepciones import ErrorValidacion, ErrorTipo
from logs import registrar_en_log


class Asesoria(Servicio):

    def __init__(self, nombre, descripcion, tarifa_base, disponible,
                 estado_servicio, especialidad, modalidad, duracion_minutos):

        super().__init__(
            nombre, descripcion, tarifa_base, disponible, estado_servicio
        )

        self.validarParametros(especialidad, modalidad, duracion_minutos)

        self.__especialidad = especialidad
        self.__modalidad = modalidad
        self.__duracion_minutos = duracion_minutos
    # validamos parametros de la entrada de variables: especialidad, modalidad y duracion_minutos
    def validarParametros(self, especialidad, modalidad, duracion_minutos):
        try:
            if not isinstance(especialidad, str) or not especialidad.strip():
                raise TypeError("La especialidad debe ser un texto no vacio.")
            if not isinstance(modalidad, str):
                raise TypeError("La modalidad debe ser un texto.")
            if modalidad not in ("Presencial", "Virtual"):
                raise ValueError("La modalidad debe ser 'Presencial' o 'Virtual'.")
            if isinstance(duracion_minutos, bool) or not isinstance(duracion_minutos, int):
                raise TypeError("La duracion debe ser un entero.")
            if duracion_minutos <= 0:
                raise ValueError("La duracion debe ser mayor a 0.")
        except TypeError as e:
            registrar_en_log(f"Error de tipo en asesoria: {e}")
            raise ErrorTipo(f"Error de tipo en datos de la asesoria: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en asesoria: {e}")
            raise ErrorValidacion(f"Error de validacion en datos de la asesoria: {e}") from e

    def calcularCosto(self, horas, impuesto=0.0, descuento=0.0):

        self._validarCalculo(horas, impuesto, descuento)

        costo = self.getTarifaBase() * horas
        costo += costo * impuesto
        costo -= costo * descuento

        return round(costo, 2)

    def describirServicio(self):

        return (
            f"Asesoría: {self.getNombre()}\n"
            f"Especialidad: {self.__especialidad}\n"
            f"Modalidad: {self.__modalidad}\n"
            f"Duración: {self.__duracion_minutos} minutos\n"
            f"Descripción: {self.getDescripcion()}\n"
            f"Tarifa base: ${self.getTarifaBase()}"
        )

    def getEspecialidad(self):
        return self.__especialidad

    def getModalidad(self):
        return self.__modalidad

    def getDuracionMinutos(self):
        return self.__duracion_minutos

    def getInformacion(self):
        return super().getInformacion() + [self.__especialidad, self.__modalidad, self.__duracion_minutos]
