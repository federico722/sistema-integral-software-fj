# equipo.py
from servicio import Servicio
from excepciones import ErrorValidacion, ErrorTipo, OperacionNoPermitida
from logs import registrar_en_log


class Equipo(Servicio):
    def __init__(self, nombre, descripcion, tarifa_base, disponible, estado_servicio, tipo_equipo, cantidad_disponible):
        super().__init__(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        self.validarParametros(tipo_equipo, cantidad_disponible)
        self.__tipo_equipo = tipo_equipo
        self.__cantidad_disponible = cantidad_disponible
    # metodo para validar los parametros del equipo antes de asignarlos
    def validarParametros(self, tipo_equipo, cantidad_disponible):
        try:
            if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
                raise TypeError("El tipo de equipo debe ser texto no vacio.")
            if isinstance(cantidad_disponible, bool) or not isinstance(cantidad_disponible, int): 
                raise TypeError("La cantidad disponible debe ser un entero.")
            if cantidad_disponible < 0:
                raise ValueError("La cantidad disponible no puede ser negativa.")
        except TypeError as e:
            registrar_en_log(f"Error de tipo en equipo: {str(e)}")
            raise ErrorTipo(f"Error de tipo en datos del equipo: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en equipo: {str(e)}")
            raise ErrorValidacion(f"Error de validacion en datos del equipo: {e}") from e
    # sobrecarga con parametros opcionales y validacion de unidades
    def calcularCosto(self, horas, impuesto = 0.0, descuento = 0.0, unidades=1):
        self._validarCalculo(horas, impuesto, descuento)
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades <= 0:
            registrar_en_log(f"Unidades invalidas en {self.getNombre()}: {unidades}")
            raise ErrorValidacion("Las unidades deben ser un entero mayor a 0.") 
        if unidades > self.__cantidad_disponible:
            registrar_en_log(f"Se pidieron {unidades} unidades de {self.getNombre()} "
                             f"y solo hay {self.__cantidad_disponible}.")
            raise OperacionNoPermitida(
                f"Solo hay {self.__cantidad_disponible} unidades disponibles.")
        costo = self.getTarifaBase() * horas * unidades
        costo -= costo * descuento
        costo += costo * impuesto
        return round(costo,2)
    # metodo para describir el servicio de equipo
    def describirServicio(self):
        return (f"Equipo '{self.getNombre()}' de tipo {self.__tipo_equipo}, "
                f"cantidad disponible: {self.__cantidad_disponible}.")

    def getInformacion(self):
        return super().getInformacion() + [self.__tipo_equipo, self.__cantidad_disponible]