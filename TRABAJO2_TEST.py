
# Función para imprimir el tablero de ajedrez
def imprimir_tablero(tablero):
    for fila in tablero:
        print('_____________________________________')
        print(' | '.join(fila))


# Función para verificar si una casilla es válida y no ha sido visitada
def es_casilla_valida(tablero, fila, columna):
    return 0 <= fila < 8 and 0 <= columna < 8 and tablero[fila][columna] == 0

def recorrido_caballo(tablero, fila, columna, paso):
    if paso == 64:  # Se han visitado todas las casillas
        return True

    movimientos = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    for df, dc in movimientos:
        nueva_fila = fila + df
        nueva_columna = columna + dc

        if es_casilla_valida(tablero, nueva_fila, nueva_columna):
            tablero[nueva_fila][nueva_columna] = paso
            if recorrido_caballo(tablero, nueva_fila, nueva_columna, paso + 1):
                return True
            tablero[nueva_fila][nueva_columna] = 0  # Retroceder si no se encontró una solución

    return False

# Crear el tablero de ajedrez vacío
tablero = [[0 for _ in range(8)] for _ in range(8)]

# Pedir al usuario la casilla de inicio
while True:
    fila_inicial = int(input("Ingresa la fila inicial del caballo (1-8): "))
    letra_inicial = str(input("Ingresa la columna inicial del caballo (A-H): "))
    if letra_inicial == 'a' or 'A':
        columna_inicial = 0
    if letra_inicial == 'b' or 'B':
        columna_inicial = 1
    if letra_inicial == 'c' or 'C':
        columna_inicial = 2
    if letra_inicial == 'd' or 'D':
        columna_inicial = 3
    if letra_inicial == 'e' or 'E':
        columna_inicial = 4
    if letra_inicial == 'f' or 'F':
        columna_inicial = 5
    if letra_inicial == 'g' or 'G':
        columna_inicial = 6
    if letra_inicial == 'h' or 'H':
        columna_inicial = 7
    
    if 0 <= fila_inicial < 8 and 0 <= columna_inicial < 8:
        break
    else:
        print("Posición no válida. Inténtalo de nuevo.")

# Empezar el recorrido del caballo desde la casilla de inicio
tablero[fila_inicial][columna_inicial] = 1

# Realizar el recorrido del caballo
if recorrido_caballo(tablero, fila_inicial, columna_inicial, 2):
    # Mostrar el tablero con los números del 01 al 64
    for i in range(8):
        for j in range(8):
            tablero[i][j] = f"{tablero[i][j]:02d}"
    imprimir_tablero(tablero)
else:
    print("No se encontró una solución.")


