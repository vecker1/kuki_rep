def crear_matriz(m, n):
    """Crea una matriz vacía de tamaño MxN."""
    return [['.' for _ in range(n)] for _ in range(m)]

def colocar_h(matriz, fila, columna):
    """Coloca una 'H' horizontalmente en la matriz, si es posible."""
    if columna + 1 < len(matriz[0]) and matriz[fila][columna] == '.' and matriz[fila][columna + 1] == '.':
        matriz[fila][columna] = 'H'
        matriz[fila][columna + 1] = 'H'
        return True
    return False

def colocar_v(matriz, fila, columna):
    """Coloca una 'V' verticalmente en la matriz, si es posible."""
    if fila + 1 < len(matriz) and matriz[fila][columna] == '.' and matriz[fila + 1][columna] == '.':
        matriz[fila][columna] = 'V'
        matriz[fila + 1][columna] = 'V'
        return True
    return False

def es_solucion_valida(matriz):
    """Verifica si una solución es válida según las condiciones dadas."""
    m, n = len(matriz), len(matriz[0])
    
    # Verificar el primer criterio: Todas las filas y columnas deben estar interrumpidas por al menos una pieza de dominó
    def verificar_interrupcion():
        # Verificar cada fila
        for i in range(m):
            hay_dominó_en_fila = False
            for j in range(n):
                if matriz[i][j] in ['H', 'V']:
                    hay_dominó_en_fila = True
                    break
            if not hay_dominó_en_fila:
                return False
        
        # Verificar cada columna
        for j in range(n):
            hay_dominó_en_columna = False
            for i in range(m):
                if matriz[i][j] in ['H', 'V']:
                    hay_dominó_en_columna = True
                    break
            if not hay_dominó_en_columna:
                return False
        
        return True
    
    # Verificar el segundo criterio: Las piezas de dominó deben cortar las líneas de separación
    def verificar_corte():
        # Verificar cada fila
        for i in range(m):
            for j in range(n - 1):
                # Verificar que la pieza de dominó "H" corta una línea vertical
                if matriz[i][j] == 'H' and matriz[i][j + 1] == 'H':
                    return True
        
        # Verificar cada columna
        for j in range(n):
            for i in range(m - 1):
                # Verificar que la pieza de dominó "V" corta una línea horizontal
                if matriz[i][j] == 'V' and matriz[i + 1][j] == 'V':
                    return True
        
        return False
    
    # Verificar ambos criterios
    return verificar_interrupcion() and verificar_corte()


def backtracking(m, n, fila, columna, matriz, soluciones):
    """Realiza el backtracking para encontrar soluciones válidas."""
    # Si hemos alcanzado el final de la matriz, verificamos la solución
    if fila == m:
        if es_solucion_valida(matriz):
            # Añade una copia profunda de la matriz a las soluciones válidas
            soluciones.append([row[:] for row in matriz])
        return
    
    # Calcular la siguiente fila y columna para el backtracking
    siguiente_fila = fila + (columna + 2) // n
    siguiente_columna = (columna + 2) % n
    
    # Colocar 'H' en la posición actual y continuar con el backtracking
    if colocar_h(matriz, fila, columna):
        backtracking(m, n, siguiente_fila, siguiente_columna, matriz, soluciones)
        # Deshacer la colocación de 'H' para continuar explorando otras opciones
        matriz[fila][columna] = '.'
        matriz[fila][columna + 1] = '.'
    
    # Colocar 'V' en la posición actual y continuar con el backtracking
    if colocar_v(matriz, fila, columna):
        backtracking(m, n, siguiente_fila, siguiente_columna, matriz, soluciones)
        # Deshacer la colocación de 'V' para continuar explorando otras opciones
        matriz[fila][columna] = '.'
        matriz[fila + 1][columna] = '.'
    
    # Continuar sin colocar ni 'H' ni 'V' en la posición actual
    backtracking(m, n, siguiente_fila, siguiente_columna, matriz, soluciones)

def mostrar_soluciones(soluciones):
    """Muestra todas las soluciones encontradas."""
    if soluciones:
        print(f"Se encontraron {len(soluciones)} soluciones válidas:")
        for i, solucion in enumerate(soluciones, start=1):
            print(f"Solución {i}:")
            mostrar_matriz(solucion)
    else:
        print("No se encontraron soluciones válidas.")

def mostrar_matriz(matriz):
    """Muestra una matriz en un formato legible con líneas de separación."""
    n = len(matriz[0])
    for i, fila in enumerate(matriz):
        # Mostrar una línea de separación entre filas
        if i > 0:
            print("-" * (4 * n + 1))
        
        # Mostrar los elementos de la fila con separación vertical
        print("| " + " | ".join(fila) + " |")
    
    # Mostrar una línea de separación al final
    print("-" * (4 * n + 1))


def main():
    # Solicitar al usuario el tamaño de la matriz
    m = int(input("Ingrese el número de filas de la matriz: "))
    n = int(input("Ingrese el número de columnas de la matriz: "))
    
    # Crear una matriz vacía y una lista para las soluciones válidas
    matriz = crear_matriz(m, n)
    soluciones = []
    
    # Iniciar el backtracking para buscar soluciones válidas
    backtracking(m, n, 0, 0, matriz, soluciones)
    
    # Mostrar las soluciones encontradas
    mostrar_soluciones(soluciones)

# Ejecutar el programa principal
main()