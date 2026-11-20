
from fase4 import Cliente
from logs import registrar_en_log
from excepciones import ErrorValidacion, ClienteNoEncontrado

class SistemaGestionCliente:

    def __init__(self):
        self.__clientes = []

    # registrar cliente 
    def registrarCliente(self, nombre, documento, correo, telefono):
        # error que origina el gestor: lo registra el gestor
        # verifica si el cliente existe
        if self.verificarClienteExistente(documento):
            # registramos el error si intenta registrar un documento duplicado
            registrar_en_log(f"Intento de registrar documento duplicado: {documento}")
            raise ErrorValidacion("El cliente ya se encuentra registrado.")
        # creamos un nuevo cliente
        nuevo_cliente = Cliente(nombre, documento, correo, telefono)  # Cliente registra los suyos
        self.__clientes.append(nuevo_cliente) # agrega cliente al final de la lista
        registrar_en_log(f"EVENTO: cliente registrado: {nuevo_cliente.getNombre()}.")
        return nuevo_cliente

    def verificarClienteExistente(self, documento):
        return self.buscarCliente(documento) is not None

    def buscarCliente(self, documento):
        try:
            for cliente in self.__clientes:
                if cliente.getInformacion() == documento:
                    return cliente
            return None

        except Exception as e:
            registrar_en_log(f"Error al buscar cliente: {e}")
            raise

    def listarClientes(self):
        return self.__clientes.copy()

    def actualizarCliente(self, documento, nombre=None,
                          nuevo_documento=None, correo=None, telefono=None):
        try:
            cliente = self.buscarCliente(documento)

            if cliente is None:
                raise ClienteNoEncontrado("No se encontró el cliente.")

            if (nuevo_documento is not None
                    and nuevo_documento != documento
                    and self.buscarCliente(nuevo_documento) is not None):
                raise ValueError("El nuevo documento ya está registrado.")

            cliente.editarInformacion(
                nombre=nombre,
                documento=nuevo_documento,
                correo=correo,
                telefono=telefono
            )
            return True

        except Exception as e:
            registrar_en_log(f"Error al actualizar cliente: {e}")
            raise

    def eliminarCliente(self, documento):
        try:
            cliente = self.buscarCliente(documento)

            if cliente is None:
                raise ClienteNoEncontrado("No se encontró el cliente.")

            self.__clientes.remove(cliente)
            registrar_en_log(f"EVENTO: Cliente eliminado: {cliente.getNombre()}")
            return True

        except Exception as e:
            registrar_en_log(f"Error al eliminar cliente: {e}")
            raise
    
    def cantidadClientes(self):
        return len(self.__clientes)
