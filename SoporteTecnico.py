# Archivo: SoporteTecnico.py
#
# Servicio especializado (hijo de Servicio) para soporte tecnico de equipos.
# Es un archivo NUEVO: no modifica ninguna clase existente del proyecto.
#
# COMO CONECTARLO (para SistemaGestion / Interfaz):
#     from SoporteTecnico import SoporteTecnico
#
#     # tipo_soporte acepta: Preventivo, Correctivo o Urgente
#     servicio = SoporteTecnico(nombre, descripcion, tarifa_base, disponible,
#                               estado_servicio, tipo_equipo, tipo_soporte)
#     sistema.obtenerGestorServicios().registrarServicio(servicio)
#
# Como hereda de Servicio, SistemaGestionServicio lo acepta sin cambios y
# se usa igual que Sala, Equipo o Asesoria (polimorfismo).
#
# PRUEBAS: python SoporteTecnico.py

# importamos la clase abstracta Servicio desde su modulo (igual que se hizo en Asesoria.py)
from servicio import Servicio
# importamos las excepciones personalizadas del proyecto
from excepciones import ErrorTipo, ErrorValidacion
# importamos la funcion que guarda los errores en el archivo de logs
from logs import registrar_en_log


# clase hija de Servicio: representa un servicio de soporte tecnico para equipos
class SoporteTecnico(Servicio):

    # tipos de soporte permitidos y el recargo que se aplica a la tarifa base.
    # (supuesto del grupo: se puede cambiar sin tocar el resto del codigo)
    RECARGOS_SOPORTE = {"Preventivo": 0.0, "Correctivo": 0.20, "Urgente": 0.35}

    def __init__(self, nombre, descripcion, tarifa_base, disponible,
                 estado_servicio, tipo_equipo, tipo_soporte):
        # el constructor de la clase padre valida y guarda los datos generales del servicio
        super().__init__(nombre, descripcion, tarifa_base, disponible, estado_servicio)
        # validamos los datos propios del soporte tecnico antes de guardarlos
        self.validarParametros(tipo_equipo, tipo_soporte)
        # guardamos los atributos privados (encapsulamiento), sin espacios y con formato uniforme
        self.__tipo_equipo = tipo_equipo.strip()
        self.__tipo_soporte = tipo_soporte.strip().capitalize()

    # getters: unica forma de leer los atributos privados desde fuera de la clase
    def getTipoEquipo(self):
        return self.__tipo_equipo

    def getTipoSoporte(self):
        return self.__tipo_soporte

    # sobrescribe getInformacion de Servicio agregando los datos propios del soporte tecnico
    def getInformacion(self):
        return super().getInformacion() + [self.__tipo_equipo, self.__tipo_soporte]

    # metodo abstracto de Servicio: valida los parametros propios de esta clase hija
    def validarParametros(self, tipo_equipo, tipo_soporte):
        try:
            # el tipo de equipo debe ser texto
            if not isinstance(tipo_equipo, str):
                raise TypeError("El tipo de equipo debe ser texto.")
            # y no puede estar vacio
            if not tipo_equipo.strip():
                raise ValueError("El tipo de equipo no puede estar vacio.")
            # el tipo de soporte tambien debe ser texto
            if not isinstance(tipo_soporte, str):
                raise TypeError("El tipo de soporte debe ser texto.")
            # y debe ser uno de los tipos permitidos (sin importar mayusculas/minusculas)
            if tipo_soporte.strip().capitalize() not in self.RECARGOS_SOPORTE:
                raise ValueError("El tipo de soporte debe ser uno de: "
                                 + ", ".join(self.RECARGOS_SOPORTE) + ".")
        except TypeError as e:
            # registramos el error en el log y lo convertimos en excepcion personalizada (encadenamiento)
            registrar_en_log(f"Error de tipo en soporte tecnico: {str(e)}")
            raise ErrorTipo(f"Error de tipo en datos del soporte tecnico: {e}") from e
        except ValueError as e:
            # igual que arriba pero para errores de valor
            registrar_en_log(f"Error de validacion en soporte tecnico: {str(e)}")
            raise ErrorValidacion(f"Error de validacion en datos del soporte tecnico: {e}") from e
        else:
            # si no hubo ningun error la validacion fue exitosa
            return True

    # metodo abstracto sobrescrito (polimorfismo). Sobrecarga con parametros opcionales:
    # calcularCosto(2) / calcularCosto(2, impuesto=0.19) / calcularCosto(2, 0.19, 0.10)
    def calcularCosto(self, horas, impuesto=0.0, descuento=0.0):
        # reutilizamos la validacion de horas, impuesto y descuento definida en Servicio
        self._validarCalculo(horas, impuesto, descuento)
        # costo base: tarifa por la cantidad de horas
        costo = self.getTarifaBase() * horas
        # recargo segun el tipo de soporte (Preventivo, Correctivo o Urgente)
        costo += costo * self.RECARGOS_SOPORTE[self.__tipo_soporte]
        # descuento: 0.10 = 10 % (mismo orden de calculo que Sala y Equipo)
        costo -= costo * descuento
        # impuesto: 0.19 = 19 %
        costo += costo * impuesto
        # redondeamos a 2 decimales
        return round(costo, 2)

    # metodo abstracto sobrescrito: describe el servicio en texto
    def describirServicio(self):
        return (f"Soporte tecnico '{self.getNombre()}' ({self.__tipo_soporte}) "
                f"para equipos tipo {self.__tipo_equipo}. "
                f"Recargo por tipo de soporte: {self.RECARGOS_SOPORTE[self.__tipo_soporte]:.0%}.")


# ==========================================================
# PRUEBAS (se ejecutan solo si corremos este archivo directamente)
# ==========================================================
if __name__ == "__main__":
    # importamos lo necesario solo para las pruebas
    from fase4 import probar
    from sala import Sala
    from cliente import Cliente
    from reserva import Reserva
    from sistema_gestion_servicio import SistemaGestionServicio

    # ===== Casos validos =====
    soporte = SoporteTecnico("Soporte Portatiles", "Mantenimiento general de portatiles",
                             60000, True, "Activo", "Portatil", "Preventivo")
    urgente = SoporteTecnico("Soporte Urgente", "Atencion inmediata en sitio",
                             60000, True, "Activo", "Servidor", "urgente")

    probar("1. Describir soporte preventivo", lambda: soporte.describirServicio())
    probar("2. Costo 2h sin extras", lambda: soporte.calcularCosto(2))
    probar("3. Costo 2h con IVA 19% y descuento 10%",
           lambda: soporte.calcularCosto(2, impuesto=0.19, descuento=0.10))
    probar("4. Costo soporte urgente 2h (recargo 35%)", lambda: urgente.calcularCosto(2))
    probar("5. Tipo de soporte normalizado ('urgente' -> 'Urgente')", lambda: urgente.getTipoSoporte())

    # ===== Errores al crear el servicio =====
    probar("6. Tipo de soporte inexistente",
           lambda: SoporteTecnico("Soporte X", "Soporte con tipo invalido", 60000, True, "Activo", "Portatil", "Magico"))
    probar("7. Tipo de equipo vacio",
           lambda: SoporteTecnico("Soporte Y", "Soporte sin tipo de equipo", 60000, True, "Activo", "   ", "Correctivo"))
    probar("8. Tipo de equipo como numero",
           lambda: SoporteTecnico("Soporte Z", "Soporte con equipo numerico", 60000, True, "Activo", 123, "Correctivo"))
    probar("9. Tarifa negativa (validacion heredada de Servicio)",
           lambda: SoporteTecnico("Soporte W", "Soporte con tarifa negativa", -5, True, "Activo", "Portatil", "Correctivo"))

    # ===== Errores en el calculo =====
    probar("10. Horas en cero", lambda: soporte.calcularCosto(0))
    probar("11. Descuento como texto", lambda: soporte.calcularCosto(2, descuento="10%"))

    # ===== Integracion con SistemaGestionServicio y polimorfismo =====
    gestor = SistemaGestionServicio()
    sala = Sala("Sala Norte", "Sala de juntas con proyector", 50000, True, "Activo", 10, "Piso 2")
    probar("12. Registrar soporte en el gestor", lambda: gestor.registrarServicio(soporte).getNombre())
    probar("13. Registrar otra clase de servicio en el gestor", lambda: gestor.registrarServicio(sala).getNombre())
    probar("14. Buscar soporte por nombre", lambda: gestor.buscarServicio("soporte portatiles").describirServicio())
    probar("15. Registrar un soporte con nombre repetido", lambda: gestor.registrarServicio(
        SoporteTecnico("Soporte Portatiles", "Otro soporte con el mismo nombre", 50000, True, "Activo", "Portatil", "Preventivo")))

    # ===== Integracion con Reserva (el costo lo calcula el propio servicio) =====
    cliente = Cliente("Federico Pelaez", "1104938557", "fede@ejemplo.com", "3115060154")
    reserva = Reserva(cliente, soporte, "2026-11-25", "10:00", 2)
    probar("16. Confirmar una reserva de soporte tecnico (2h, IVA 19%, dto 10%)",
           lambda: reserva.confirmarReserva(impuesto=0.19, descuento=0.10))

    print("\n--- 17. Polimorfismo: mismo metodo, distinto comportamiento ---")
    for servicio in gestor.listarServicios():
        print(f"{type(servicio).__name__}: costo 2h = {servicio.calcularCosto(2)}")