# fase4.py
from entidad_sistema import EntidadSistema
from cliente import Cliente
from servicio import Servicio
from sala import Sala
from equipo import Equipo         


def probar(titulo, accion):
    print(f"\n--- {titulo} ---")
    try:
         print(f"OK: {accion()}")
    except Exception as e:
        print(f"Error controlado ({type(e).__name__}): {e}")
        
if __name__ == "__main__":
    # ===== Casos validos =====
    sala = Sala("Sala Norte", "Sala de juntas con proyector", 50000, True, "Activo", 10, "Piso 2")
    equipo = Equipo("Proyector HD", "Proyector portatil para presentaciones", 20000, True, "Activo", "Proyector", 5)

    probar("1. Describir sala", lambda: sala.describirServicio())
    probar("2. Describir equipo", lambda: equipo.describirServicio())
    probar("3. Costo sala 2h (sin extras)", lambda: sala.calcularCosto(2))
    probar("4. Costo sala 2h, IVA 19% y descuento 10%",
           lambda: round(sala.calcularCosto(2, impuesto=0.19, descuento=0.10), 2))
    probar("5. Costo equipo 3h x 2 unidades", lambda: equipo.calcularCosto(3, unidades=2))
    probar("6. Costo equipo con IVA y descuento",
           lambda: round(equipo.calcularCosto(3, impuesto=0.19, descuento=0.10, unidades=2), 2))

    # ===== Errores al crear servicios =====
    probar("7. Tarifa negativa",
           lambda: Sala("Sala Sur", "Sala pequena para reuniones", -100, True, "Activo", 5, "Piso 1"))
    probar("8. Tarifa como texto",
           lambda: Sala("Sala Sur", "Sala pequena para reuniones", "cien", True, "Activo", 5, "Piso 1"))
    probar("9. Nombre demasiado corto",
           lambda: Equipo("PC", "Computador de escritorio completo", 15000, True, "Activo", "Computador", 3))
    probar("10. Estado de servicio invalido",
           lambda: Sala("Sala Este", "Sala amplia con tablero", 40000, True, "Roto", 8, "Piso 3"))
    probar("11. Capacidad en cero",
           lambda: Sala("Sala Oeste", "Sala sin sillas todavia", 40000, True, "Activo", 0, "Piso 3"))
    probar("12. Capacidad como texto",
           lambda: Sala("Sala Oeste", "Sala sin sillas todavia", 40000, True, "Activo", "diez", "Piso 3"))
    probar("13. Cantidad de equipos negativa",
           lambda: Equipo("Camara", "Camara profesional de video", 30000, True, "Activo", "Camara", -2))

    # ===== Errores en el calculo de costos =====
    probar("14. Horas negativas", lambda: sala.calcularCosto(-1))
    probar("15. Descuento absurdo (300%)", lambda: sala.calcularCosto(2, descuento=3))
    probar("16. Impuesto como texto", lambda: sala.calcularCosto(2, impuesto="19"))
    probar("17. Mas unidades de las disponibles", lambda: equipo.calcularCosto(2, unidades=10))
    probar("18. Unidades en cero", lambda: equipo.calcularCosto(2, unidades=0))

    # ===== Abstraccion y polimorfismo =====
    probar("19. Instanciar la clase abstracta Servicio",
           lambda: Servicio("Algo", "Descripcion de prueba", 1000, True, "Activo"))

    print("\n--- 20. Polimorfismo: mismo metodo, distinto comportamiento ---")
    for servicio in [sala, equipo]:
        print(f"{type(servicio).__name__}: {servicio.describirServicio()}")

    probar("Cliente valido", lambda: Cliente("Federico Pelaez", "1104938557", "fede@ejemplo.com", "3115060154").getInformacion())
    probar("Datos faltantes", lambda: Cliente(None, "1104938557", None, "3115060154"))
    probar("Nombre corto", lambda: Cliente("Fe", "1104938557", "fede@ejemplo.com", "3115060154"))
    probar("Documento con simbolo", lambda: Cliente("Federico Pelaez", "11#4938557", "fede@ejemplo.com", "3115060154"))
    probar("Correo sin dominio", lambda: Cliente("Federico Pelaez", "1104938557", "federicopelaez", "3115060154"))
    probar("Telefono como numero", lambda: Cliente("Federico Pelaez", "1104938557", "fede@ejemplo.com", 3115060154))
