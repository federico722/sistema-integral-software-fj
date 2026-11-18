# libreria para generar identificadores unicos
import uuid
# libreria para crear clases abstractas
from abc import ABC, abstractmethod
# clase abstracta que representa una entidad del sistema

# Excepciones personalizadas
from excepciones import ErrorValidacion, ErrorTipo, ErrorFormato, OperacionNoPermitida
from logs import registrar_en_log
class EntidadSistema(ABC):
    def __init__(self):
        # generamos un identificador unico para la entidad
        self.__idEntidad = str(uuid.uuid4())

    # metodo que retorna el identificador unico de la entidad
    def getIdEntidad(self):
        return self.__idEntidad
    @abstractmethod
    # metodo abstracto que debe ser implementado por las clases que hereden de EntidadSistema
    def getInformacion(self):
        pass

class Cliente(EntidadSistema):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # validamos la informacion antes de asignarla a los atributos
        self.validarInformacion(nombre, documento, correo, telefono)
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono
    # metodo que retorna la informacion del cliente en una lista
    def getInformacion(self):
        return [self.__nombre, self.__documento, self.__correo, self.__telefono]
    
    # metodo que retorna el identificador unico del cliente
    def getIdentificacion(self):
        return super().getIdEntidad()
    
    # metodo que permite editar la informacion del cliente, validando los datos antes de actualizarlos
    def editarInformacion(self, nombre=None, documento=None, correo=None, telefono=None):
        # validamos la informacion antes de editarla
        self.validarInformacion(nombre, documento, correo, telefono)
        # si pasaron la validacion sin lanzar error, actualizamos 
        if nombre is not None:
            self.__nombre = nombre
        if documento is not None:
            self.__documento = documento
        if correo is not None:
            self.__correo = correo
        if telefono is not None:
            self.__telefono = telefono

    # metodo que valida la informacion del cliente, lanzando excepciones personalizadas en caso de error
    def validarInformacion(self, nombre=None, documento=None, correo=None, telefono=None ):
        try:
            # 1. validar el nombre
            if nombre is not None:
                if not isinstance(nombre, str):
                    raise TypeError("El nombre debe ser una cadena de texto. ")
                if len(nombre.strip()) < 3:
                    raise ValueError("El nombre debe tener almenos 3 caracteres.")
            # 2. validar documento
            if documento is not None:
                if not isinstance(documento, str):
                    raise TypeError("El documento debe ser una cadena de texto.")
                if not documento.isdigit() or len(documento) < 5:
                    raise ValueError("El documento debe contener solo numeros (minimo 5 digitos).")
            # 3. validar correo
            if correo is not None:
                if not isinstance(correo, str):
                    raise TypeError("El correo debe ser una cadena de texto.")
                if "@" not in correo or "." not in correo.split("@")[-1]:
                    raise ValueError("El correo no tiene un formato valido (ej: usuario@dominio.com).")

            # 4. validar telefono
            if telefono is not None:
                if not isinstance(telefono, str):
                    raise TypeError("El telefono debe ser una cadena de texto.")
                if not telefono.isdigit() or len(telefono) < 7:
                    raise ValueError("El telefono debe contener solo numeros (minimo 7 digitos).")

        except TypeError as e:
             # Encadenamiento de excepciones: convertimos el error técnico en excepción personalizada
            registrar_en_log(f"Error de tipo en cliente: {str(e)}")
            raise ErrorTipo(f"Error de tipo en datos del cliente: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en cliente: {str(e)}")
            # Si el mensaje menciona 'formato' o 'números', lanzamos ErrorFormato; si no, ErrorValidacion
            if "formato" in str(e) or "numeros" in str(e):
                raise ErrorFormato(f"Error de formato en datos del cliente: {e}") from e
            raise ErrorValidacion(f"Error de validacion en datos del cliente: {e}") from e
        else:
            return True # Si no hay errores, la validación es exitosa

class Servicio(EntidadSistema):
    def __init__(self, nombre, descripcion, tarifa_base, disponible, estado_servicio):
        super().__init__()
        # validamos los parametros del servicio antes de asignarlos
        self.validarBase(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        # generamos un identificador unico para el servicio
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
    def validarBase(self, nombre, descripcion, tarifa_base, disponible, estado_servicio):
        try:
            if not isinstance(nombre, str):
                raise TypeError("El nombre debe ser una cadena de texto.")
            if len(nombre.strip()) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres.")
            if not isinstance(descripcion, str):
                raise TypeError("La descripcion debe ser una cadena de texto.")
            if len(descripcion.strip()) < 10:
                raise ValueError("La descripcion debe tener al menos 10 caracteres.")
            if not isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)):
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
    def calcularCosto(self):
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
            registrar_en_log(f"Error de validacion en sala: {str(e)}")
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
        return costo
    # describir servicio 
    def describirServicio(self):
        return (f"Sala '{self.getNombre()}' en {self.__ubicacion},"
                f"capacidad {self.__capacidad} personas.")

class Equipo(Servicio):
    def __init__(self, nombre, descripcion, tarifa_base, disponible, estado_servicio, tipo_equipo, cantidad_disponible):
        super().__init__(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        self.validarParametros(tipo_equipo, cantidad_disponible)
        self.__tipo_equipo = tipo_equipo
        self.__cantidad_disponible = cantidad_disponible

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

    def calcularCosto(self, horas, impuesto = 0.0, descuento = 0.0, unidades=1):
        self._validarCalculo(horas, impuesto, descuento)
        if unidades > self.__cantidad_disponible:
            registrar_en_log(f"Se pidieron {unidades} unidades de {self.getNombre()} "
                             f"y solo hay {self.__cantidad_disponible}.")
            raise OperacionNoPermitida(
                f"Solo hay {self.__cantidad_disponible} unidades disponibles.")
        costo = self.getTarifaBase() * horas * unidades
        costo -= costo * descuento
        costo += costo * impuesto
        return costo
    
    def describirServicio(self):
        return (f"Equipo '{self.getNombre()}' de tipo {self.__tipo_equipo}, "
                f"cantidad disponible: {self.__cantidad_disponible}.")
            
            
if __name__ == "__main__":
    # creamos una instancia de la clase cliente para probar la funcionalidad
    prueba1 = Cliente("Federico Pelaez", "1104938557","federicopelaez@ejemplo.com", "3115060154")
    # mostramos el identificador unico y la informacion del cliente
    print(f"Identificador del cliente: {prueba1.getIdEntidad()}")
    print(f"Informacion del cliente: {prueba1.getInformacion()}")

    # craemos otra instancia de la clase cliente para probar la funcionalidad con datos erroneos y capturamos la excepcion personalizada
    try:
       prueba2 = Cliente("Fe", "11#4938557","federicopelaez", "311506#154")
    except Exception as e:
       print(f"Error controlado: {e}")


