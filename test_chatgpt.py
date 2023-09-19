def crear_tablero():
    return [["  " for _ in range(8)] for _ in range(8)]

def mostrar_tablero(tablero):
    letras_columnas = "   A    B    C    D    E    F    G    H"
    separador = "-" * 42
    print(letras_columnas)
    for fila in range(7, -1, -1):
        print(f"{fila + 1}| {' | '.join(tablero[fila])} |{fila + 1}")
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
    x, y = None, None

    while True:
        try:
            x = int(input("Ingresa la fila (1-8) del caballo: ")) - 1
            columna = input("Ingresa la columna (A-H) del caballo: ").upper()
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
        movimiento += 1
        x, y = movimientos_posibles[0]
        tablero[x][y] = f"{movimiento:02d}"
        movimientos.append((x, y))
        mostrar_tablero(tablero)
        input("Presiona Enter para continuar...")

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

if __name__ == "__main__":
    main()
