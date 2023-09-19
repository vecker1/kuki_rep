def crear_tablero():
    tablero = [["  " for _ in range(8)] for _ in range(8)]
    return tablero

def mostrar_tablero(tablero):
    print("   A     B    C    D    E    F    G    H")
    for i, fila in enumerate(tablero):
        print(f"{8 - i}| {' | '.join(fila)} | {8 - i}")
        print("-" * 42)
    print("   A     B    C    D    E    F    G    H")

def calcular_movimientos(x, y):
    movimientos = []
    movimientos_posibles = [
        (-1, -2), (-2, -1), (-2, 1), (-1, 2),
        (1, -2), (2, -1), (2, 1), (1, 2)
    ]

    for dx, dy in movimientos_posibles:
        nueva_x, nueva_y = x + dx, y + dy
        if 0 <= nueva_x < 8 and 0 <= nueva_y < 8:
            movimientos.append((nueva_x, nueva_y))

    return movimientos

def main():
    tablero = crear_tablero()
    mostrar_tablero(tablero)

    while True:
        try:
            
            x = int(input("Ingresa un numero (1-8) para la fila del caballo: ")) - 1
            letra_inicial = str(input("Ingresa una letra (A-H) para la columna del caballo: ").upper())
            if letra_inicial == 'a' or 'A':
                y = 0
            if letra_inicial == 'b' or 'B':
                y = 1
            if letra_inicial == 'c' or 'C':
                y = 2
            if letra_inicial == 'd' or 'D':
                y = 3
            if letra_inicial == 'e' or 'E':
                y = 4
            if letra_inicial == 'f' or 'F':
                y = 5
            if letra_inicial == 'g' or 'G':
                y = 6
            if letra_inicial == 'h' or 'H':
                y = 7

            if 0 <= x < 8 and 0 <= y < 8:
                break
            else:
                print("Posición fuera del rango. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Debe ser un número del 1 al 8 y una letra de la A a la H.")

    tablero[x][y] = "GO"  # Marcar posición inicial con "GO"
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
        print("El caballo no puede hacer más movimientos.")
    mostrar_tablero(tablero)

if __name__ == "__main__":
    main()
