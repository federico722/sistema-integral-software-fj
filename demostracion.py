# Archivo: demostracion.py 
# simula las operaciones completas

from sistemaGestion import SistemaGestion
from sala import Sala
from equipo import Equipo
from Asesoria import Asesoria
from SoporteTecnico import SoporteTecnico
from logs import registrar_en_log

contador = 0

def operacion(titulo, accion, mostrar=None):
    """Ejecuta una operacion; si falla, el error se muestra y el programa sigue.
    'mostrar' es opcional: convierte el resultado en un texto legible."""
    global contador
    contador += 1
    print(f"\n--- Operacion {contador}: {titulo} ---")
    try:
        resultado = accion()
        print(f"OK: {mostrar(resultado) if mostrar else resultado}")
        return resultado
    except Exception as e:
        print(f"Error controlado ({type(e).__name__}): {e}")
        return None


def resumen(reserva):
    return f"reserva {reserva.getIdEntidad()[:8]} - estado {reserva.getEstado()}"


def ejecutarDemostracion():
    registrar_en_log("===== INICIO DE LA DEMOSTRACION =====")
    sistema = SistemaGestion()
    clientes = sistema.obtenerGestorClientes()
    servicios = sistema.obtenerGestorServicios()
    reservas = sistema.obtenerGestorReservas()

    # ---------- clientes ----------
    operacion("Registrar cliente valido",
              lambda: clientes.registrarCliente("Federico Pelaez", "1104938557", "fede@ejemplo.com", "3115060154").getNombre())
    operacion("Registrar segundo cliente valido",
              lambda: clientes.registrarCliente("Laura Gomez", "52963741", "laura@ejemplo.com", "3001234567").getNombre())
    operacion("Cliente con documento invalido",
              lambda: clientes.registrarCliente("Pedro Ruiz", "11#4938557", "pedro@ejemplo.com", "3115060154"))
    operacion("Cliente con datos faltantes",
              lambda: clientes.registrarCliente(None, "99887766", None, "3115060154"))
    operacion("Cliente duplicado",
              lambda: clientes.registrarCliente("Federico Pelaez", "1104938557", "fede@ejemplo.com", "3115060154"))

    # ---------- servicios ----------
    sala = operacion("Crear sala valida",
                     lambda: servicios.registrarServicio(
                         Sala("Sala Norte", "Sala de juntas con proyector", 50000, True, "Activo", 10, "Piso 2")).describirServicio())
    operacion("Crear equipo valido",
              lambda: servicios.registrarServicio(
                  Equipo("Proyector HD", "Proyector portatil para presentaciones", 20000, True, "Activo", "Proyector", 5)).describirServicio())
    operacion("Crear asesoria valida",
              lambda: servicios.registrarServicio(
                  Asesoria("Asesoria Python", "Asesoria personalizada de programacion", 80000, True, "Activo", "Programacion", "Virtual", 60)).describirServicio())
    operacion("Crear servicio con tarifa negativa",
              lambda: servicios.registrarServicio(
                  Sala("Sala Sur", "Sala pequena para reuniones", -100, True, "Activo", 5, "Piso 1")))
    operacion("Crear servicio no disponible (para probar el rechazo)",
              lambda: servicios.registrarServicio(
                  Equipo("Camara 4K", "Camara profesional de video", 30000, False, "Activo", "Camara", 2)).describirServicio())

    # ---------- calculos inconsistentes ----------
    sala_norte = servicios.buscarServicio("Sala Norte")
    operacion("Calculo con horas negativas", lambda: sala_norte.calcularCosto(-1))
    operacion("Calculo con descuento absurdo (300%)", lambda: sala_norte.calcularCosto(2, descuento=3))

    # ---------- reservas ----------
    r1 = operacion("Reserva valida de sala",
                   lambda: sistema.crearReserva("1104938557", "Sala Norte", "2026-12-01", "10:00", 2), resumen)
    operacion("Reserva que choca de horario con la anterior",
              lambda: sistema.crearReserva("52963741", "Sala Norte", "2026-12-01", "11:00", 2))
    operacion("Reserva de un servicio no disponible",
              lambda: sistema.crearReserva("1104938557", "Camara 4K", "2026-12-02", "09:00", 1))
    operacion("Reserva de un cliente inexistente",
              lambda: sistema.crearReserva("00000000", "Sala Norte", "2026-12-03", "09:00", 1))
    operacion("Reserva con fecha invalida",
              lambda: sistema.crearReserva("1104938557", "Sala Norte", "31-12-2026", "09:00", 1))
    r2 = operacion("Reserva de equipo",
                   lambda: sistema.crearReserva("52963741", "Proyector HD", "2026-12-01", "10:00", 3), resumen)

    # ---------- estados y costos ----------
    if r1:
        operacion("Confirmar sala con IVA 19% y descuento 10%",
                  lambda: r1.confirmarReserva(impuesto=0.19, descuento=0.10))
        operacion("Confirmar de nuevo la misma reserva",
                  lambda: r1.confirmarReserva())
    if r2:
        operacion("Confirmar equipo pidiendo mas unidades de las que hay",
                  lambda: r2.confirmarReserva(unidades=10))
        operacion("Confirmar equipo con 2 unidades",
                  lambda: r2.confirmarReserva(unidades=2))
        operacion("Cancelar la reserva del equipo",
                  lambda: (r2.cancelarReserva(), r2.getEstado())[1])
        operacion("Cancelar otra vez la misma reserva",
                  lambda: r2.cancelarReserva())
    if r1:
        operacion("Eliminar cliente con reserva activa",
                  lambda: sistema.eliminarCliente("1104938557"))
        operacion("Procesar la reserva confirmada",
                  lambda: (r1.procesarReserva(), r1.getEstado())[1])
        operacion("Historial de reservas del cliente",
                  lambda: [r.getEstado() for r in reservas.consultarHistorialCliente("1104938557")])

    # ---------- soporte tecnico y reglas finales ----------
    operacion("Crear soporte tecnico valido (el tipo 'urgente' se normaliza a 'Urgente')",
              lambda: servicios.registrarServicio(
                  SoporteTecnico("Soporte Portatiles", "Mantenimiento de portatiles en sitio",
                                 60000, True, "Activo", "Portatil", "urgente")).describirServicio())
    operacion("Crear soporte tecnico con un tipo de soporte que no existe",
              lambda: servicios.registrarServicio(
                  SoporteTecnico("Soporte Magico", "Soporte con un tipo que no existe",
                                 60000, True, "Activo", "Portatil", "Magico")))
    soporte = servicios.buscarServicio("Soporte Portatiles")
    operacion("Cotizar soporte urgente 2h con recargo 35%, descuento 10% e IVA 19%",
              lambda: soporte.calcularCosto(2, impuesto=0.19, descuento=0.10))
    r3 = operacion("Reserva de soporte tecnico",
                   lambda: sistema.crearReserva("1104938557", "Soporte Portatiles", "2026-12-03", "14:00", 2), resumen)
    if r3:
        operacion("Confirmar la reserva de soporte tecnico (costo calculado por el propio servicio)",
                  lambda: r3.confirmarReserva(impuesto=0.19, descuento=0.10))
    operacion("Reserva de soporte tecnico que choca de horario",
              lambda: sistema.crearReserva("52963741", "Soporte Portatiles", "2026-12-03", "15:00", 1), resumen)
    operacion("Eliminar un servicio que tiene reservas activas",
              lambda: sistema.eliminarServicio("Soporte Portatiles"))
    r4 = operacion("Reserva de sala que queda Pendiente",
                   lambda: sistema.crearReserva("52963741", "Sala Norte", "2026-12-04", "09:00", 1), resumen)
    if r4:
        operacion("Procesar una reserva que aun esta Pendiente",
                  lambda: r4.procesarReserva())
        operacion("Eliminar una reserva activa (Pendiente)",
                  lambda: reservas.eliminarReserva(r4.getIdEntidad()))
        operacion("Cancelar y despues eliminar esa misma reserva",
                  lambda: (r4.cancelarReserva(), reservas.eliminarReserva(r4.getIdEntidad()))[1])

    registrar_en_log("===== FIN DE LA DEMOSTRACION =====")
    print(f"\nDemostracion terminada: {contador} operaciones. Revise errores.log")


if __name__ == "__main__":
    ejecutarDemostracion()