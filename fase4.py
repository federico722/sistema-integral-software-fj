# libreria para generar identificadores unicos
import uuid
# libreria para crear clases abstractas
from abc import ABC, abstractmethod
# clase abstracta que representa una entidad del sistema

# Excepciones personalizadas
class ErrorValidacion(Exception):
    pass

class ErrorTipo(ErrorValidacion):
    pass

class ErrorFormato(ErrorValidacion):
    pass
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
        return self.super().getIdEntidad()
    
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
            raise ErrorTipo(f"Error de tipo en datos del cliente: {e}") from e
        except ValueError as e:
            # Si el mensaje menciona 'formato' o 'números', lanzamos ErrorFormato; si no, ErrorValidacion
            if "formato" in str(e) or "numeros" in str(e):
                raise ErrorFormato(f"Error de formato en datos del cliente: {e}") from e
            raise ErrorValidacion(f"Error de validacion en datos del cliente: {e}") from e
        else:
            return True # Si no hay errores, la validación es exitosa
        
# creamos una instancia de la clase cliente para probar la funcionalidad
prueba1 = Cliente("Federico Pelaez", "1104938557","federicopelaez@ejemplo.com", "3115060154")
# mostramos el identificador unico y la informacion del cliente
print(f"Identificador del cliente: {prueba1.getIdEntidad()}")
print(f"Informacion del cliente: {prueba1.getInformacion()}")

# craemos otra instancia de la clase cliente para probar la funcionalidad con datos erroneos y capturamos la excepcion personalizada
prueba2 = Cliente("Fe", "11#4938557","federicopelaez", "311506#154")

