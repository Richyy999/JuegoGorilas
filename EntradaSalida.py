import Tablero

import os


clear = lambda: os.system("cls")

def imprimirTablero(tablero):
    clear()
    
    for fila in range(tablero.shape[0]):
        linea = ""
        for columna in range(tablero.shape[1]):
            linea += tablero[fila, columna]
        
        print(linea)

def imprimirGorila(gorila):
    if gorila == Tablero.GORILA_A:
        print("Gorila A:")
    else:
        print("Gorila B:")


def pedirDatos(tablero, gorila, velMax, velMin, angMax, angMin):

    velCorrecta = True
    vel = 0
    while vel > velMax or vel < velMin:
        imprimirTablero(tablero)
        imprimirGorila(gorila)
        if not velCorrecta:
            print("Velocidad no válida")
            
        print(f"La velocidad debe estar entre {velMax}m/s y {velMin}m/s")
        try:
            vel = float(input("Introduce la velocidad (m/s): ").replace(",", "."))
            velCorrecta = True
        except ValueError:
            velCorrecta = False
    
    anguloCorrecto = True
    angulo = -1
    while angulo > angMax or angulo < angMin:
        imprimirTablero(tablero)
        imprimirGorila(gorila)
        if not anguloCorrecto:
            print("Ángulo incorrecto")
            
        print(f"Introduce la velocidad (m/s): {vel}")
        print(f"El ángulo debe estar entre {angMax}º y {angMin}º")
        try:
            angulo = float(input("Introduce el ángulo: ").replace(",", "."))
            anguloCorrecto = True
        except ValueError:
            anguloCorrecto = False
    
    return vel, angulo


def mostrarGanador(ganador, victoriaGorilaA, victoriaGorilaB):
    if ganador == victoriaGorilaA:
        print("¡El gorila A ha ganado!")
    elif ganador == victoriaGorilaB:
        print("¡El gorila B ha ganado!")
    
