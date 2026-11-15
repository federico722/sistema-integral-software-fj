# Archivo: menu.py

# Importamos lo que necesitamos (al final, cuando unamos todo, descomentaremos estas líneas)
# from reserva import Reserva
# from logs import registrar_en_log

def mostrar_menu():
 
    print("   SISTEMA SOFTWARE FJ - MENÚ PRINCIPAL")
  
    print("1. Registrar un nuevo Cliente")
    print("2. Crear una Reserva")
    print("3. Ver Registro de Errores (Logs)")
    print("4. Salir del sistema")

def ejecutar_menu():
    while True: # Este bucle hace que el menú se repita hasta que el usuario elija salir
        mostrar_menu()
        
        try:
            # Pedimos la opción al usuario
            opcion = input("Seleccione una opción (1-4): ")
            
            # Validamos que sea un número
            opcion_num = int(opcion) 
            
            if opcion_num == 1:
                print("\n--> Iniciando registro de cliente...")
                # Aquí iría la lógica para pedir los datos del cliente
                print("Cliente registrado con éxito (Simulación).")
                
            elif opcion_num == 2:
                print("\n--> Iniciando creación de reserva...")
                # Aquí iría la lógica para crear una reserva usando tu clase Reserva
                print("Reserva procesada con éxito (Simulación).")
                
            elif opcion_num == 3:
                print("\n--> Mostrando archivo de errores.log...")
                try:
                    # Intentamos abrir el archivo de logs para leerlo
                    with open("errores.log", "r", encoding="utf-8") as archivo:
                        print(archivo.read())
                except FileNotFoundError:
                    print("Aún no hay errores registrados en el archivo.")
                    
            elif opcion_num == 4:
                print("\nSaliendo del sistema. ¡Hasta pronto!")
                break # Rompe el bucle y sale del programa
                
            else:
                print("Opción no válida. Por favor, elija un número del 1 al 4.")
                
        except ValueError:
            # ESTO ES CLAVE: Si el usuario escribe "hola" en vez de un número, atrapamos el error
            print("Error: Por favor, ingrese solo números (1, 2, 3 o 4).")
            
        except Exception as e:
            # Atrapamos cualquier otro error inesperado
            print(f"Ocurrió un error inesperado: {e}")

# Esto asegura que el menú solo se ejecute si corremos este archivo directamente
if __name__ == "__main__":
    ejecutar_menu()
