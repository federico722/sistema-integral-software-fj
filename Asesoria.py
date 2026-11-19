
from fase4 import Servicio


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

    def validarParametros(self, especialidad, modalidad, duracion_minutos):

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValueError("La especialidad debe ser un texto válido.")

        if modalidad not in ("Presencial", "Virtual"):
            raise ValueError("La modalidad debe ser Presencial o Virtual.")

        if (isinstance(duracion_minutos, bool)
                or not isinstance(duracion_minutos, int)
                or duracion_minutos <= 0):
            raise ValueError("La duración debe ser un número entero positivo.")

        return True

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
