import numpy
import random

TAMANO_TABLERO = 20

SIN_IMPACTO = 0
IMPACTO_BORDE = 1
IMPACTO_FUERA = 2
IMPACTO_EDIFICIO = 3
IMPACTO_GORILA_A = 4
IMPACTO_GORILA_B = 5

BORDE = "|"
BORDE_ABAJO = "###"
EDIFICIO = " # "
VACIO = "   "
TRAYECTORIA = " · "
IMPACTO = " * "
GORILA_A = " A "
GORILA_B = " B "


def crearTablero():
    if TAMANO_TABLERO <= 5:
        raise ValueError(None, "El tablero debe ser, como mínimo, de 6 x 6")

    tablero = numpy.zeros((TAMANO_TABLERO, TAMANO_TABLERO), 'U3')

    for i in range(TAMANO_TABLERO):
        for j in range(TAMANO_TABLERO):
            if esBorde(i, j):
                tablero[i, j] = BORDE
            elif esBordeAbajo(i, j):
                tablero[i, j] = BORDE_ABAJO
            else:
                tablero[i, j] = VACIO

    return tablero


def esBorde(fila, columna):
    return columna == 0 or columna == TAMANO_TABLERO - 1


def esBordeAbajo(fila, columna):
    return fila == TAMANO_TABLERO - 1


def getCelda(tablero, columna, fila):
    filas = tablero.shape[1] - 1
    fila = filas - fila

    return tablero[fila, columna]


def getAnchuraLibre(tablero):
    fila = TAMANO_TABLERO - 2
    casillasVacias = 0

    for columna in range(TAMANO_TABLERO):
        celda = tablero[fila, columna]
        if celda == VACIO:
            casillasVacias += 1

    return casillasVacias


def ajustarAltura(tablero, columnas, altura, casilla):
    for columna in columnas:
        for fila in range(TAMANO_TABLERO - 2, TAMANO_TABLERO - 2 - altura, -1):
            tablero[fila, columna] = casilla


def crearEdificios(tablero):
    columnaEdificio = 1
    anchuraLibre = getAnchuraLibre(tablero)
    while (anchuraLibre > 0):
        altura = random.randrange(1, TAMANO_TABLERO - 2)
        anchura = random.randrange(4)
        while (anchura > anchuraLibre):
            anchura = random.randrange(1, 4)

        columnas = list(range(columnaEdificio, columnaEdificio + anchura))
        ajustarAltura(tablero, columnas, altura, EDIFICIO)
        columnaEdificio += anchura

        anchuraLibre = getAnchuraLibre(tablero)


def situarGorila(tablero, columna, gorila):
    for fila in range(TAMANO_TABLERO - 2):
        if tablero[fila + 1, columna] == EDIFICIO:
            tablero[fila, columna] = gorila
            return


def crearGorilas(tablero):
    tercio = int(TAMANO_TABLERO / 3)

    columnaGorilaA = random.randrange(1, tercio + 1)
    situarGorila(tablero, columnaGorilaA, GORILA_A)

    columnaGorilaB = random.randrange(tercio * 2, TAMANO_TABLERO - 1)
    situarGorila(tablero, columnaGorilaB, GORILA_B)


def getPosicionGorila(tablero, gorila):
    y, x = 0, 0
    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            if tablero[fila, columna] == gorila:
                y, x = fila, columna

    return x, y


def mostrarTrayectoria(tablero, x, y, gorila):
    xGorila, yGorila = getPosicionGorila(tablero, gorila)
    x, y = x + xGorila, yGorila - y
    if y < 0:
        return IMPACTO_FUERA
    if y >= TAMANO_TABLERO - 1 or x <= 0 or x >= TAMANO_TABLERO - 1:
        return IMPACTO_BORDE

    casilla = tablero[y, x]
    if casilla == VACIO or casilla == TRAYECTORIA:
        tablero[y, x] = TRAYECTORIA
        return SIN_IMPACTO

    elif casilla == EDIFICIO:
        tablero[y, x] = IMPACTO
        return IMPACTO_EDIFICIO

    elif casilla == GORILA_A:
        return IMPACTO_GORILA_A

    elif casilla == GORILA_B:
        return IMPACTO_GORILA_B


def bajarGorila(tablero, columna, gorila):
    for fila in range(TAMANO_TABLERO - 1):
        if tablero[fila + 1, columna] == EDIFICIO:
            tablero[fila, columna] = gorila


def eliminarEdificio(tablero, fila, columna, gorila):
    vacio = False
    casilla = tablero[fila, columna]
    if casilla == GORILA_A or casilla == GORILA_B:
        bajarGorila(tablero, columna, gorila)
        
    elif casilla != IMPACTO:
        if casilla == VACIO:
            vacio = True
            
        tablero[fila, columna] = VACIO
    
    return vacio

def limpiarProyectil(tablero):
    for fila in range(TAMANO_TABLERO):
        for columna in range(TAMANO_TABLERO):
            if tablero[fila, columna] == TRAYECTORIA or tablero[fila, columna] == IMPACTO:
                tablero[fila, columna] = VACIO

def getCoordenadas(tablero, x, y, gorila):
    xGorila, yGorila = getPosicionGorila(tablero, gorila)
    columna, fila = x + xGorila, yGorila - y
    
    return columna, fila