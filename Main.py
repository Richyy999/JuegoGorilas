import Tablero
import EntradaSalida

import math
import time

GRAVEDAD = 9.8
INCREMENTO = 0.01

VEL_MAXIMA = 80
VEL_MINIMA = 1

ANGULO_MAX = 90
ANGULO_MIN = 0

EN_CURSO = 0
VICTORIA_GORILA_A = 1
VICTORIA_GORILA_B = 2


def disparar(tablero, gorila, vel, ang):
    ang = math.radians(ang)
    tiempo = 0
    resultado = Tablero.SIN_IMPACTO
    xAntes, yAntes = -1, -1
    primerImpacto = True
    while resultado == Tablero.SIN_IMPACTO:
        x = vel * math.cos(ang) * tiempo
        y = vel * math.sin(ang) * tiempo - GRAVEDAD * tiempo * tiempo

        x, y = int(x), int(y)

        if gorila == Tablero.GORILA_B:
            x = -x
        
        resultado = Tablero.mostrarTrayectoria(tablero, x, y, gorila)
        tiempo += INCREMENTO
        
        if x == 0 and y == 0 and primerImpacto:
            resultado = Tablero.SIN_IMPACTO
        
        if x != xAntes or y != yAntes:
            EntradaSalida.imprimirTablero(tablero)
            time.sleep(0.1)

            xAntes, yAntes = x, y

            if x != 0 or y != 0:
                primerImpacto = False

    return xAntes, yAntes, resultado


def eliminarEdificio(tablero, x, y, gorila):
    x, y = Tablero.getCoordenadas(tablero, x, y, gorila)
    for i in range(y, -1, -1):
        vacio, gorilaBajado = Tablero.eliminarEdificio(tablero, i, x, gorila)
        if not vacio:
            EntradaSalida.imprimirTablero(tablero)
            time.sleep(0.1)
        
        if gorilaBajado:
            return


def jugar():
    tablero = Tablero.crearTablero()
    Tablero.crearEdificios(tablero)
    Tablero.crearGorilas(tablero)

    EntradaSalida.imprimirTablero(tablero)

    resultado = EN_CURSO

    gorilaA = Tablero.GORILA_A
    gorilaB = Tablero.GORILA_B

    while resultado == EN_CURSO:
        vel, ang = EntradaSalida.pedirDatos(tablero, gorilaA, VEL_MAXIMA, VEL_MINIMA, ANGULO_MAX, ANGULO_MIN)
        Tablero.limpiarProyectil(tablero)
        x, y, resDisparo = disparar(tablero, Tablero.GORILA_A, vel, ang)

        if resDisparo == Tablero.IMPACTO_GORILA_A:
            resultado = VICTORIA_GORILA_B
            continue

        elif resDisparo == Tablero.IMPACTO_GORILA_B:
            resultado = VICTORIA_GORILA_A
            continue

        elif resDisparo == Tablero.IMPACTO_EDIFICIO:
            eliminarEdificio(tablero, x, y, Tablero.GORILA_A)

        vel, ang = EntradaSalida.pedirDatos(tablero, gorilaB, VEL_MAXIMA, VEL_MINIMA, ANGULO_MAX, ANGULO_MIN)
        Tablero.limpiarProyectil(tablero)
        x, y, resDisparo = disparar(tablero, Tablero.GORILA_B, vel, ang)


        if resDisparo == Tablero.IMPACTO_GORILA_A:
            resultado = VICTORIA_GORILA_B

        elif resDisparo == Tablero.IMPACTO_GORILA_B:
            resultado = VICTORIA_GORILA_A
        
        elif resDisparo == Tablero.IMPACTO_EDIFICIO:
            eliminarEdificio(tablero, x, y, Tablero.GORILA_B)

    return resultado


try:
    ganador = jugar()

    EntradaSalida.mostrarGanador(ganador, VICTORIA_GORILA_A, VICTORIA_GORILA_B)
except KeyboardInterrupt:
    pass

finally:
    input("\nFin del juego.\nPulsa Enter para salir")
