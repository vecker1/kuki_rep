import time

def crear_tablero():
    return [["  " for _ in range(8)] for _ in range(8)]

def mostrar_tablero(tablero):
    separador = "_" * 44
    print(" ")
    letras_columnas = "    A     B    C    D    E    F    G    H"
    print(separador)
    print(letras_columnas)
    print(separador)
    for fila in range(7, -1, -1):
        print(f"{fila + 1}|  {' | '.join(tablero[fila])} |{fila + 1}")
        print(separador)
    print(letras_columnas)

def calcular_movimientos(x, y):
    movimientos_posibles = [
        (-1, -2), (-2, -1), (-2, 1), (-1, 2),
        (1, -2), (2, -1), (2, 1), (1, 2)
    ]
    return [(x + dx, y + dy) for dx, dy in movimientos_posibles if 0 <= x + dx < 8 and 0 <= y + dy < 8]

def main():
    tablero = crear_tablero()
    mostrar_tablero(tablero)

    x, y = None, None

    while True:
        try:
            print(" ")
            print("*"*50)
            print("********Eligir posicion inicial del caballo*******")
            print("*"*50)
            print("**POSICION INICIO: [GO] | POSICION CABALLO: [CA]**")
            print("*"*50)
            print(" ")
            x = int(input("Ingresa un numero para la fila (1-8) del caballo: ")) - 1
            columna = input("Ingresa una letra para la columna (A-H) del caballo: ").upper()
            if 0 <= x < 8 and columna in "ABCDEFGH":
                y = ord(columna) - ord('A')
                break
            else:
                print("Posición fuera del rango. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Debe ser un número del 1 al 8 y una letra de la A a la H.")

    tablero[x][y] = "GO"
    movimientos = [(x, y)]
    movimiento = 0

    while movimiento < 63:
        movimientos_posibles = calcular_movimientos(x, y)
        movimientos_posibles = [(nx, ny) for nx, ny in movimientos_posibles if (nx, ny) not in movimientos]
        if not movimientos_posibles:
            break
        x, y = movimientos_posibles[0]
        movimiento += 1
        tablero[x][y] = "CA"
        movimientos.append((x, y))
        mostrar_tablero(tablero)
        time.sleep(0.5)  # Espera 1.5 segundos para ver el movimiento
        tablero[x][y] = f"{movimiento:02d}"

    if movimiento == 63:
        print("El caballo ha completado todos los movimientos posibles.")
    else:
        print('')
        print("*"*48)
        print("*"*48)
        print("***El caballo no puede hacer más movimientos.***")
        print("*"*48)
        print("*"*48)
    mostrar_tablero(tablero)
    print(" ")
    print("Total de movimientos hechos:", f'{movimiento}')
    time.sleep(300)

if __name__ == "__main__":
    main()

