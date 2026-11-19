
# Archivo: sistema_gestion_cliente.py

from fase4 import Cliente
from logs import registrar_en_log


class SistemaGestionCliente:
    """
    Clase encargada de administrar los clientes del sistema.
    """

    def __init__(self):
        self.__clientes = []

    def registrarCliente(self, nombre, documento, correo, telefono):
        try:
            # Evitar registrar documentos repetidos
            for cliente in self.__clientes:
                if cliente.getInformacion()[1] == documento:
                    raise ValueError("El cliente ya se encuentra registrado.")

            nuevo_cliente = Cliente(
                nombre,
                documento,
                correo,
                telefono
            )

            self.__clientes.append(nuevo_cliente)
            return nuevo_cliente

        except (ValueError, TypeError) as e:
            registrar_en_log(f"Error al registrar cliente: {e}")
            raise

        except Exception as e:
            registrar_en_log(f"Error inesperado al registrar cliente: {e}")
            raise

    def buscarCliente(self, documento):
        try:
            for cliente in self.__clientes:
                if cliente.getInformacion()[1] == documento:
                    return cliente

            return None

        except Exception as e:
            registrar_en_log(f"Error al buscar cliente: {e}")
            raise

    def listarClientes(self):
        return self.__clientes.copy()

    def actualizarCliente(
        self,
        documento,
        nombre=None,
        nuevo_documento=None,
        correo=None,
        telefono=None
    ):
        try:
            cliente = self.buscarCliente(documento)

            if cliente is None:
                raise ValueError("No se encontró el cliente.")

            if (
                nuevo_documento is not None
                and nuevo_documento != documento
                and self.buscarCliente(nuevo_documento) is not None
            ):
                raise ValueError("El nuevo documento ya está registrado.")

            cliente.editarInformacion(
                nombre=nombre,
                documento=nuevo_documento,
                correo=correo,
                telefono=telefono
            )

            return True

        except (ValueError, TypeError) as e:
            registrar_en_log(f"Error al actualizar cliente: {e}")
            raise

        except Exception as e:
            registrar_en_log(f"Error inesperado al actualizar cliente: {e}")
            raise

    def eliminarCliente(self, documento):
        try:
            cliente = self.buscarCliente(documento)

            if cliente is None:
                raise ValueError("No se encontró el cliente.")

            self.__clientes.remove(cliente)
            return True

        except (ValueError, TypeError) as e:
            registrar_en_log(f"Error al eliminar cliente: {e}")
            raise

        except Exception as e:
            registrar_en_log(f"Error inesperado al eliminar cliente: {e}")
            raise

    def cantidadClientes(self):
        return len(self.__clientes)
