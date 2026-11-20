# sala.py
from servicio import Servicio
from excepciones import ErrorValidacion, ErrorTipo
from logs import registrar_en_log

        
class Sala(Servicio):
    def __init__(self, nombre, descripcion, tarifa_base, disponible, estado_servicio, capacidad, ubicacion):
        super().__init__(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        self.validarParametros(capacidad, ubicacion)
        self.__capacidad = capacidad
        self.__ubicacion = ubicacion

    def validarParametros(self, capacidad, ubicacion):
        try:
            if isinstance(capacidad, bool) or not isinstance(capacidad, int):
                raise TypeError("La capacidad debe ser un entero.")
            if capacidad <= 0:
                raise ValueError("La capacidad debe ser mayor a 0.")
            if not isinstance(ubicacion, str) or not ubicacion.strip():
                raise TypeError("La ubicacion debe ser texto no vacio.")
        except TypeError as e:
            registrar_en_log(f"Error de Tipo en sala: {str(e)}")
            raise ErrorTipo(f"Error de tipo en datos de la sala: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en sala: {str(e)}")
            raise ErrorValidacion(f"Error de validacion en datos de la sala: {e}") from e

    # sobrecarga con parametros opcionales
    def calcularCosto(self, horas, impuesto = 0.0, descuento = 0.0):
        self._validarCalculo(horas, impuesto, descuento)
        costo = self.getTarifaBase() * horas
        costo -= costo * descuento # descuento: 0.10 = 10 %
        costo += costo * impuesto # impuesto: 0.19 = 19 %
        return round(costo,2)
    
    # describir servicio 
    def describirServicio(self):
        return (f"Sala '{self.getNombre()}' en {self.__ubicacion}, "
                f"capacidad {self.__capacidad} personas.")

    def getInformacion(self):
        return super().getInformacion() + [self.__capacidad, self.__ubicacion]
