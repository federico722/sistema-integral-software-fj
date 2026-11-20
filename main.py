#  main.py  -> punto de entrada del programa interactivo

from sistemaGestion import SistemaGestion
from interfaz import Interfaz

if __name__ == "__main__":
    Interfaz(SistemaGestion()).ejecutar()