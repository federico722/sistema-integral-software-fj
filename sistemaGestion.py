# sistemaGestion.py
from sistema_gestion_cliente import SistemaGestionCliente
from sistema_gestion_servicio import SistemaGestionServicio
from sistemaGestionReserva import SistemaGestionReserva, ESTADOS_ACTIVOS
from reserva import Reserva
from logs import registrar_en_log
from excepciones import ClienteNoEncontrado, ServicioNoEncontrado, OperacionNoPermitida

class sistemaGestion:
    """Conecta los tres gestores y coordina las reglas que involucran a mas de uno."""

    def __init__(self):
        # se crean UNA sola vez aqui, asi todos comparten las mismas listas
        self.gestor_clientes = SistemaGestionCliente()
        self.gestor_Servicios = SistemaGestionServicio()
        self.gestor_reservas = SistemaGestionReserva()

    def obtenerGestorClientes(self):
        return self.__gestor_clientes
    
    def obtenerGestorServicios(self):
        return self.__gestor_servicios

    def obtenerGestorReserva(self):
        return self.__gestor_reservas

    # ---------- operaciones que cruzan gestores ----------
    def crearReserva(self, documento_cliente, identificacion_servicio,
                     fecha, hora_inicio, duracion_horas):
        cliente = self.__gestor_clientes.buscarCliente(documento_cliente)
        if cliente is None:
            registrar_en_log(f"Reserva rechazada: cliente inexistente ({documento_cliente}).")
            raise ClienteNoEncontrado("No se encontró un cliente con ese documento.")

        servicio = self.__gestor_servicios.buscarServicio(identificacion_servicio)
        if servicio is None:
            registrar_en_log(f"Reserva rechazada: servicio inexistente ({identificacion_servicio}).")
            raise ServicioNoEncontrado("No se encontró el servicio solicitado.")

        # Reserva valida sus propios datos; el gestor verifica que el horario este libre
        reserva = Reserva(cliente, servicio, fecha, hora_inicio, duracion_horas)
        return self.__gestor_reservas.registrarReserva(reserva)

    def eliminarCliente(self, documento):
        activas = [r for r in self.__gestor_reservas.consultarHistorialCliente(documento)
                   if r.getEstado() in ESTADOS_ACTIVOS]
        if activas:
            registrar_en_log(f"Eliminacion rechazada: el cliente {documento} tiene reservas activas.")
            raise OperacionNoPermitida("No se puede eliminar un cliente con reservas activas.")
        return self.__gestor_clientes.eliminarCliente(documento)

    def eliminarServicio(self, identificacion):
        servicio = self.__gestor_servicios.buscarServicio(identificacion)
        if servicio is not None:
            activas = [r for r in self.__gestor_reservas.listarReservas()
                        if r.getServicio() is servicio and r.getEstado() in ESTADOS_ACTIVOS]
            if activas:
                registrar_en_log(f"Eliminacion rechazada: {servicio.getNombre()} tiene reservas activas.")
                raise OperacionNoPermitida("No se puede eliminar un servicio con reservas activas.")
        return self.__gestor_servicios.eliminarServicio(identificacion)

    


        
