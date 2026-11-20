# cliente.py
from entidad_sistema import EntidadSistema
from excepciones import ErrorValidacion, ErrorTipo, ErrorFormato
from logs import registrar_en_log

class Cliente(EntidadSistema):
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # validamos la informacion antes de asignarla a los atributos
        self.validarInformacion(nombre, documento, correo, telefono, obligatorios=True)
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono
    # metodo que retorna la informacion del cliente en una lista
    def getInformacion(self):
        return [self.__nombre, self.__documento, self.__correo, self.__telefono]
    
    # metodo que retorna el identificador unico del cliente
    def getIdentificacion(self):
        return self.getIdEntidad()

    def getCorreo(self):
        return self.__correo

    def getTelefono(self):
        return self.__telefono

    def getDocumento(self):
        return self.__documento

    def getNombre(self):
        return self.__nombre
    
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
    def validarInformacion(self, nombre=None, documento=None, correo=None, telefono=None, obligatorios=False ):
        try:
            if obligatorios:
                datos = {"nombre": nombre, "documento": documento,
                     "correo": correo, "telefono": telefono}
                faltantes = [campo for campo, valor in datos.items() if valor is None]
                if faltantes:
                    raise ValueError(f"Faltan datos obligatorios: {', '.join(faltantes)}")
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
                    raise ErrorFormato("El documento debe contener solo numeros (minimo 5 digitos).")
            # 3. validar correo
            if correo is not None:
                if not isinstance(correo, str):
                    raise TypeError("El correo debe ser una cadena de texto.")
                if "@" not in correo or "." not in correo.split("@")[-1]:
                    raise ErrorFormato("El correo no tiene un formato valido (ej: usuario@dominio.com).")

            # 4. validar telefono
            if telefono is not None:
                if not isinstance(telefono, str):
                    raise TypeError("El telefono debe ser una cadena de texto.")
                if not telefono.isdigit() or len(telefono) < 7:
                    raise ErrorFormato("El telefono debe contener solo numeros (minimo 7 digitos).")
        # excepciones de formato, error de tipo y error de valor
        except ErrorFormato as e:
            # ya es una excepcion personalizada: solo la registramos y la dejamos pasar
            registrar_en_log(f"Error de formato en cliente: {e}")
            raise
        except TypeError as e:
            registrar_en_log(f"Error de tipo en cliente: {e}")
            raise ErrorTipo(f"Error de tipo en datos del cliente: {e}") from e
        except ValueError as e:
            registrar_en_log(f"Error de validacion en cliente: {e}")
            raise ErrorValidacion(f"Error de validacion en datos del cliente: {e}") from e
        else:
            return True

