# entidad_sistema.py
import uuid
from abc import ABC, abstractmethod

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
