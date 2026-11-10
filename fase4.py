# libreria para generar identificadores unicos
import uuid
# liberaria para crear clases abstractas
from abc import ABC, abstractmethod
# clase abstracta que representa una entidad del sistema
class EntidadSistema(ABC):
    def __init__(self):
        # generamos un identificador unico para la entidad
        self.__idEntidad = str(uuid.uuid4())
    # metodo abstracto que debe ser implementado por las clases que hereden de EntidadSistema
    @abstractmethod
    def getIdEntidad(self):
        return self.__idEntidad
    @abstractmethod
    # metodo abstracto que debe ser implementado por las clases que hereden de EntidadSistema
    def getInformacion(self):
        pass

# clase temporal que sirve para provar la clase abstracta EntidadSistema
class test(EntidadSistema):
    def __init__(self):
        super().__init__()

    def getIdEntidad(self):
        return self._EntidadSistema__idEntidad
    
    def getInformacion(self):
        msg = "*"*70
        msg += "\nInformacion de la entidad del sistema"
        msg += f"\nID de la entidad: {self.getIdEntidad()}"
        msg += f"\n{'*'*70}"
        return msg

# creamos una instancia de la clase test y probamos los metodos getIdEntidad y getInformacion
prueba1 = test()
print(f"ID de la entidad: {prueba1.getIdEntidad()}")
print(prueba1.getInformacion())