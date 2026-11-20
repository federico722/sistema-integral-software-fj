# servicio.py
from abc import abstractmethod
from entidad_sistema import EntidadSistema
from excepciones import ErrorValidacion, ErrorTipo
from logs import registrar_en_log

class Servicio(EntidadSistema):
    def __init__(self, nombre, descripcion, tarifa_base, disponible, estado_servicio):
        super().__init__()
        # validamos los parametros del servicio antes de asignarlos
        self._validarBase(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__tarifa_base = tarifa_base
        self.__disponible = disponible
        self.__estado_servicio = estado_servicio

    #getters
    def getNombre(self): return self.__nombre
    def getDescripcion(self): return self.__descripcion
    def getTarifaBase(self): return self.__tarifa_base
    def getDisponible(self): return self.__disponible
    def getEstadoServicio(self): return self.__estado_servicio
    def getInformacion(self):
        return [self.__nombre, self.__descripcion, self.__tarifa_base, self.__disponible, self.__estado_servicio]

    # metodo para validar los parametros del servicio antes de asignarlos
    def _validarBase(self, nombre, descripcion, tarifa_base, disponible, estado_servicio):
        try:
            if not isinstance(nombre, str):
                raise TypeError("El nombre debe ser una cadena de texto.")
            if len(nombre.strip()) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres.")
            if not isinstance(descripcion, str):
                raise TypeError("La descripcion debe ser una cadena de texto.")
            if len(descripcion.strip()) < 10:
                raise ValueError("La descripcion debe tener al menos 10 caracteres.")
            if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)):
                raise TypeError("La tarifa base debe ser un numero.")
            if tarifa_base <= 0:
                raise ValueError("La tarifa base debe ser mayor a 0.")
           
            if not isinstance(disponible, bool):
                raise TypeError("El estado de disponibilidad debe ser True o False.")
         
            if not isinstance(estado_servicio, str):
                raise TypeError("El estado del servicio debe ser una cadena de texto.")
            if estado_servicio not in ["Activo", "Inactivo"]:
                raise ValueError("El estado del servicio debe ser 'Activo' o 'Inactivo'.")

        except TypeError as e:
            registrar_en_log(f"Error de tipo en servicio: {str(e)}")
            raise ErrorTipo(f"Error de tipo en datos del servicio: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en servicio: {str(e)}")
            raise ErrorValidacion(f"Error de validacion en datos del servicio: {e}") from e
    # tres metodos abstractos calcularCosto, describirServicio y validarParametros
    @abstractmethod
    def calcularCosto(self, horas, impuesto=0.0, descuento=0.0):
        pass
    @abstractmethod
    def describirServicio(self):
        pass
    @abstractmethod
    def validarParametros(self):
        pass

    # metodo para validar la entrada de descuento, impuesto y horas 
    def _validarCalculo(self, horas, impuesto, descuento):
        try:
            if isinstance(horas, bool) or not isinstance(horas, (int, float)):
                raise TypeError("Las horas deben ser un numero.")
            if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
                raise TypeError("El impuesto debe ser un numero.")
            if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
                raise TypeError("El descuento debe ser un numero.")
            if horas <= 0:
                raise ValueError("Las horas deben ser mayores a 0.")
            if not 0 <= impuesto <= 1:
                raise ValueError("El impuesto debe estar entre 0 y 1.")
            if not 0 <= descuento <= 1:
                raise ValueError("El descuento debe estar entre 0 y 1.")
        except TypeError as e:
            registrar_en_log(f"Error de tipo en calculo de costo: {self.getNombre()}: {e}")
            raise ErrorTipo(f"Error de tipo en el calculo de costo: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en el calculo de costo: {self.getNombre()}: {e}")
            raise ErrorValidacion(f"Error de validacion en el calculo de costo: {e}") from e

    def puedeReservarse(self):
        return self.__disponible and self.__estado_servicio == "Activo"
        