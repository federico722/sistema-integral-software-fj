# interfaz.py
from excepciones import ErrorSistema, ErrorTipo, ErrorValidacion
from logs import registrar_en_log, leer_log
from sala import Sala
from equipo import Equipo
from Asesoria import Asesoria
from SoporteTecnico import SoporteTecnico

class Interfaz:
    """Menus por consola. Solo habla con SistemaGestion; no contiene reglas de negocio."""
    def __init__(self, sistema):
        self.__sistema = sistema

    # =====================================================
    # Entrada y salida
    # =====================================================
    def solicitarTexto(self, mensaje):
        return input(mensaje).strip()

    def solicitarOpcional(self, mensaje):
        """Devuelve None si el usuario presiona Enter (sirve para editar datos)."""
        texto = input(f"{mensaje} (Enter para omitir): ").strip()
        return texto if texto else None

    def solicitarNumero(self, mensaje, tipo=float, defecto=None):
        texto = input(mensaje).strip()
        if texto == "" and defecto is not None:
            return defecto
        try:
            return tipo(texto)
        except ValueError as e:
            registrar_en_log(f"Entrada numerica invalida en la interfaz: '{texto}'")
            raise ErrorTipo(f"'{texto}' no es un numero valido.") from e

    def solicitarPorcentaje(self, mensaje):
        """El usuario escribe 19 y el sistema usa 0.19. Enter equivale a 0."""
        return self.solicitarNumero(f"{mensaje} en % (Enter = 0): ", float, defecto=0.0) / 100

    def solicitarSiNo(self, mensaje):
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        raise ErrorValidacion("Responda 's' o 'n'.")

    def mostrarResultados(self, *lineas):
        for linea in lineas:
            print(linea)

    def _formatearReserva(self, reserva):
        (id_, cliente, servicio, fecha, h_ini, h_fin,
         duracion, costo, estado) = reserva.getInformacion()
        return (f"[{id_[:8]}] {cliente} | {servicio} | {fecha} {h_ini}-{h_fin} "
                f"({duracion} h) | ${costo:,.2f} | {estado}")

    # =====================================================
    # Manejo central de errores: nada detiene el programa
    # =====================================================
    def _ejecutarSeguro(self, accion):
        try:
            accion()
        except ErrorSistema as e:
            # errores propios: ya los registro quien los origino, aqui solo se muestran
            print(f"\n[!] No se pudo completar la operacion: {e}")
        except Exception as e:
            # errores no previstos: aqui si se registran
            registrar_en_log(f"Error inesperado en la interfaz: {type(e).__name__}: {e}")
            print("\n[!] Ocurrio un error inesperado. Quedo registrado en el log.")

    def _submenu(self, titulo, opciones):
        while True:
            print(f"\n=== {titulo} ===")
            for numero, (texto, _) in enumerate(opciones, start=1):
                print(f"{numero}. {texto}")
            print("0. Volver")
            eleccion = input("Seleccione una opcion: ").strip()
            if eleccion == "0":
                return
            if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
                self._ejecutarSeguro(opciones[int(eleccion) - 1][1])
            else:
                print("Opcion no valida.")

    # =====================================================
    # Menus
    # =====================================================
    def mostrarMenuPrincipal(self):
        print("\n==============================================")
        print("   SOFTWARE FJ - SISTEMA DE GESTION")
        print("==============================================")
        print("1. Clientes")
        print("2. Servicios")
        print("3. Reservas")
        print("4. Ver registro de eventos y errores (log)")
        print("0. Salir")

    def mostrarMenuClientes(self):
        self._submenu("CLIENTES", [
            ("Registrar cliente", self._registrarCliente),
            ("Buscar cliente por documento", self._buscarCliente),
            ("Listar clientes", self._listarClientes),
            ("Editar cliente", self._editarCliente),
            ("Eliminar cliente", self._eliminarCliente),
        ])

    def mostrarMenuServicios(self):
        self._submenu("SERVICIOS", [
            ("Registrar sala", lambda: self._registrarServicio("sala")),
            ("Registrar equipo", lambda: self._registrarServicio("equipo")),
            ("Registrar asesoria", lambda: self._registrarServicio("asesoria")),
            ("Registrar soporte tecnico", lambda: self._registrarServicio("soporte")),
            ("Listar servicios", self._listarServicios),
            ("Cotizar el costo de un servicio", self._cotizarServicio),
            ("Eliminar servicio", self._eliminarServicio),
        ])

    def mostrarMenuReservas(self):
        self._submenu("RESERVAS", [
            ("Crear reserva", self._crearReserva),
            ("Confirmar reserva", self._confirmarReserva),
            ("Cancelar reserva", self._cancelarReserva),
            ("Procesar (finalizar) reserva", self._procesarReserva),
            ("Listar reservas", self._listarReservas),
            ("Historial de un cliente", self._historialCliente),
            ("Eliminar reserva", self._eliminarReserva),
        ])

    def _verLog(self):
        contenido = leer_log()
        print("\n--- Registro de eventos y errores ---")
        print(contenido if contenido else "Aun no hay registros.")

    # =====================================================
    # Clientes
    # =====================================================
    def _registrarCliente(self):
        nombre = self.solicitarTexto("Nombre completo: ")
        documento = self.solicitarTexto("Documento (solo numeros): ")
        correo = self.solicitarTexto("Correo: ")
        telefono = self.solicitarTexto("Telefono (solo numeros): ")
        cliente = self.__sistema.obtenerGestorClientes().registrarCliente(
            nombre, documento, correo, telefono)
        self.mostrarResultados(f"\nCliente registrado: {cliente.getNombre()}")

    def _buscarCliente(self):
        documento = self.solicitarTexto("Documento a buscar: ")
        cliente = self.__sistema.obtenerGestorClientes().buscarCliente(documento)
        if cliente is None:
            self.mostrarResultados("\nNo hay un cliente con ese documento.")
        else:
            nombre, doc, correo, tel = cliente.getInformacion()
            self.mostrarResultados(f"\n{nombre} | doc {doc} | {correo} | tel {tel}")

    def _listarClientes(self):
        clientes = self.__sistema.obtenerGestorClientes().listarClientes()
        if not clientes:
            self.mostrarResultados("\nNo hay clientes registrados.")
            return
        print()
        for cliente in clientes:
            nombre, doc, correo, tel = cliente.getInformacion()
            print(f"- {nombre} | doc {doc} | {correo} | tel {tel}")

    def _editarCliente(self):
        documento = self.solicitarTexto("Documento del cliente a editar: ")
        print("Deje en blanco lo que no quiera cambiar.")
        nombre = self.solicitarOpcional("Nuevo nombre")
        nuevo_doc = self.solicitarOpcional("Nuevo documento")
        correo = self.solicitarOpcional("Nuevo correo")
        telefono = self.solicitarOpcional("Nuevo telefono")
        self.__sistema.obtenerGestorClientes().actualizarCliente(
            documento, nombre, nuevo_doc, correo, telefono)
        self.mostrarResultados("\nCliente actualizado.")

    def _eliminarCliente(self):
        documento = self.solicitarTexto("Documento del cliente a eliminar: ")
        self.__sistema.eliminarCliente(documento)
        self.mostrarResultados("\nCliente eliminado.")

    # =====================================================
    # Servicios
    # =====================================================

    def _registrarServicio(self, tipo):
        nombre = self.solicitarTexto("Nombre del servicio: ")
        descripcion = self.solicitarTexto("Descripcion (minimo 10 caracteres): ")
        tarifa = self.solicitarNumero("Tarifa base por hora: ", float)
        disponible = self.solicitarSiNo("¿Esta disponible?")
        estado = self.solicitarTexto("Estado (Activo/Inactivo): ").capitalize()

       
        if tipo == "sala":
            capacidad = self.solicitarNumero("Capacidad (personas): ", int)
            ubicacion = self.solicitarTexto("Ubicacion: ")
            servicio = Sala(nombre, descripcion, tarifa, disponible, estado, capacidad, ubicacion)
        elif tipo == "equipo":
            tipo_equipo = self.solicitarTexto("Tipo de equipo: ")
            cantidad = self.solicitarNumero("Cantidad disponible: ", int)
            servicio = Equipo(nombre, descripcion, tarifa, disponible, estado, tipo_equipo, cantidad)
        elif tipo == "asesoria":
            especialidad = self.solicitarTexto("Especialidad: ")
            modalidad = self.solicitarTexto("Modalidad (Presencial/Virtual): ").capitalize()
            minutos = self.solicitarNumero("Duracion en minutos: ", int)
            servicio = Asesoria(nombre, descripcion, tarifa, disponible, estado,
                                especialidad, modalidad, minutos)
        elif tipo == "soporte":
            tipo_equipo = self.solicitarTexto("Tipo de equipo: ")
            tipo_soporte = self.solicitarTexto("Tipo de soporte (Preventivo/Correctivo/Urgente): ")
            servicio = SoporteTecnico(nombre, descripcion, tarifa, disponible, estado,
                                      tipo_equipo, tipo_soporte)
        # pendiente registrar otro servicio de reserva

        self.__sistema.obtenerGestorServicios().registrarServicio(servicio)
        self.mostrarResultados(f"\nServicio registrado: {servicio.getNombre()}")

    def _listarServicios(self):
        servicios = self.__sistema.obtenerGestorServicios().listarServicios()
        if not servicios:
            self.mostrarResultados("\nNo hay servicios registrados.")
            return
        print()
        for servicio in servicios:
            estado = "reservable" if servicio.puedeReservarse() else "NO reservable"
            print(f"- {servicio.describirServicio()}  Tarifa ${servicio.getTarifaBase():,.2f}/h  [{estado}]")

    def _cotizarServicio(self):
        identificacion = self.solicitarTexto("Nombre del servicio: ")
        servicio = self.__sistema.obtenerGestorServicios().buscarServicio(identificacion)
        if servicio is None:
            self.mostrarResultados("\nNo hay un servicio con ese nombre.")
            return
        horas = self.solicitarNumero("Horas: ", float)
        impuesto = self.solicitarPorcentaje("Impuesto")
        descuento = self.solicitarPorcentaje("Descuento")
        opciones = self._opcionesPropias(servicio)
        costo = servicio.calcularCosto(horas, impuesto, descuento, **opciones)
        self.mostrarResultados(f"\nCosto estimado: ${costo:,.2f}")

    def _eliminarServicio(self):
        identificacion = self.solicitarTexto("Nombre del servicio a eliminar: ")
        self.__sistema.eliminarServicio(identificacion)
        self.mostrarResultados("\nServicio eliminado.")

    # es necesario modificarlo al agregar opciones propias en algun servicio 
    def _opcionesPropias(self, servicio):
        """Datos extra que solo algunos servicios usan al calcular el costo (ej. unidades de un equipo)."""
        if isinstance(servicio, Equipo):
            return {"unidades": self.solicitarNumero("Unidades (Enter = 1): ", int, defecto=1)}
        return {}

    # =====================================================
    # Reservas
    # =====================================================
    def _crearReserva(self):
        documento = self.solicitarTexto("Documento del cliente: ")
        servicio = self.solicitarTexto("Nombre del servicio: ")
        fecha = self.solicitarTexto("Fecha (AAAA-MM-DD): ")
        hora = self.solicitarTexto("Hora de inicio (HH:MM): ")
        duracion = self.solicitarNumero("Duracion en horas: ", float)
        reserva = self.__sistema.crearReserva(documento, servicio, fecha, hora, duracion)
        self.mostrarResultados("\nReserva creada (queda Pendiente):", self._formatearReserva(reserva))

    def _confirmarReserva(self):
        gestor = self.__sistema.obtenerGestorReservas()
        reserva = gestor.obtenerReserva(self.solicitarTexto("Id de la reserva: "))
        impuesto = self.solicitarPorcentaje("Impuesto")
        descuento = self.solicitarPorcentaje("Descuento")
        opciones = self._opcionesPropias(reserva.getServicio())
        costo = reserva.confirmarReserva(impuesto, descuento, **opciones)
        self.mostrarResultados(f"\nReserva confirmada. Costo total: ${costo:,.2f}")

    def _cancelarReserva(self):
        gestor = self.__sistema.obtenerGestorReservas()
        reserva = gestor.obtenerReserva(self.solicitarTexto("Id de la reserva: "))
        reserva.cancelarReserva()
        self.mostrarResultados("\nReserva cancelada.")

    def _procesarReserva(self):
        gestor = self.__sistema.obtenerGestorReservas()
        reserva = gestor.obtenerReserva(self.solicitarTexto("Id de la reserva: "))
        reserva.procesarReserva()
        self.mostrarResultados("\nReserva procesada (Finalizada).")

    def _listarReservas(self):
        reservas = self.__sistema.obtenerGestorReservas().listarReservas()
        if not reservas:
            self.mostrarResultados("\nNo hay reservas registradas.")
            return
        print()
        for reserva in reservas:
            print(self._formatearReserva(reserva))

    def _historialCliente(self):
        documento = self.solicitarTexto("Documento del cliente: ")
        reservas = self.__sistema.obtenerGestorReservas().consultarHistorialCliente(documento)
        if not reservas:
            self.mostrarResultados("\nEse cliente no tiene reservas.")
            return
        print()
        for reserva in reservas:
            print(self._formatearReserva(reserva))

    def _eliminarReserva(self):
        gestor = self.__sistema.obtenerGestorReservas()
        gestor.eliminarReserva(self.solicitarTexto("Id de la reserva: "))
        self.mostrarResultados("\nReserva eliminada.")

    # =====================================================
    # Bucle principal
    # =====================================================
    def ejecutar(self):
        opciones = {
            "1": self.mostrarMenuClientes,
            "2": self.mostrarMenuServicios,
            "3": self.mostrarMenuReservas,
            "4": self._verLog,
        }
        try:
            while True:
                self.mostrarMenuPrincipal()
                eleccion = input("Seleccione una opcion: ").strip()
                if eleccion == "0":
                    print("\nSaliendo del sistema. ¡Hasta pronto!")
                    break
                accion = opciones.get(eleccion)
                if accion is None:
                    print("Opcion no valida.")
                else:
                    self._ejecutarSeguro(accion)
        except (KeyboardInterrupt, EOFError):
            print("\n\nEntrada cerrada. Saliendo del sistema.")

