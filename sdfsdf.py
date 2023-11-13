import random
import heapq

grafo = {
    '1': ['2', '4'],
    '2': ['1', '3'],
    '3': ['2', '9', '14', '15'],
    '4': ['1', '5'],
    '5': ['4', '6'],
    '6': ['5', '7'],
    '7': ['6', '8'],
    '8': ['7'],
    '9': ['3', '10'],
    '10': ['9', '17', '16'],
    '11': ['12', '17'],
    '12': ['11', '18'],
    '13': ['14', '20'],
    '14': ['3', '13', '22'],
    '15': ['3', '23', '27', '16'],
    '16': ['10', '15'],
    '17': ['10', '11', '27'],
    '18': ['12', '19', '28', '29'],
    '19': ['18'],
    '20': ['13', '21' , '24'],
    '21': ['20', '22'],
    '22': ['21', '23'],
    '23': ['15', '22'],
    '24': ['20', '25', '30', '31'],
    '25': ['22', '24'],
    '26': ['27', '31'],
    '27': ['15', '17', '26', '33'],
    '28': ['18', '34'],
    '29': ['18', '35'],
    '30': ['24', '36'],
    '31': ['24', '26', '32'],
    '32': ['31', '37'],
    '33': ['27', '34', '42'],
    '34': ['28', '33', '38'],
    '35': ['29', '38'],
    '36': ['30', '37', '39'],
    '37': ['32', '36', '41'],
    '38': ['34', '35', '42'],
    '39': ['36', '40'],
    '40': ['39', '41'],
    '41': ['40', '42'],
    '42': ['41', '38']
}

nodos_llave = ['19', '38', '41']
nodo_llave = random.choice(nodos_llave)
nodo_heroe = '1'
nodo_bruja = '8'
nodo_anterior_heroe = None
nodo_anterior_bruja = None
nodo_anterior = None

def tirar_dado():
    caras = [
        (3, 1),  # Cara 1: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 2: Mueve al héroe 1 y a la bruja 1
        (2, 0),  # Cara 3: Mueve al héroe 2 y a la bruja 0
        (3, 1),  # Cara 4: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 5: Mueve al héroe 1 y a la bruja 1
        (0, 2)   # Cara 6: Mueve al héroe 3 y a la bruja 2
    ]
    resultado = random.choice(caras)
    print("Dado:", resultado)
    return resultado

def encontrar_camino_mas_corto(grafo, inicio, destino):
    # Implementación del algoritmo de Dijkstra para encontrar el camino más corto
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    heap = [(0, inicio)]

    while heap:
        distancia_actual, nodo_actual = heapq.heappop(heap)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino in grafo[nodo_actual]:
            distancia_nueva = distancia_actual + 1  # Considerando que cada arista tiene peso 1
            if distancia_nueva < distancias[vecino]:
                distancias[vecino] = distancia_nueva
                heapq.heappush(heap, (distancia_nueva, vecino))

    # Reconstruir el camino
    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = distancias[actual] - 1  # Retroceder un paso

    return camino[:-1]  # Excluir el último elemento para evitar duplicados en el movimiento de la bruja

def seguir_camino_bruja(nodo_actual, nodo_llave, nodo_anterior_bruja):
    # Obtener el camino más corto hacia la llave
    camino_mas_corto = encontrar_camino_mas_corto(grafo, nodo_actual, nodo_llave)

    # Elegir el siguiente nodo en el camino (o quedarse en el mismo nodo si ya está en la llave)
    if len(camino_mas_corto) > 1:
        # Eliminar el nodo anterior del héroe de las opciones disponibles
        opciones_disponibles = [nodo for nodo in camino_mas_corto[1:] if nodo != nodo_anterior_bruja]
        siguiente_nodo = random.choice(opciones_disponibles) if opciones_disponibles else nodo_actual
    else:
        siguiente_nodo = nodo_actual

    print(f"La bruja se mueve al nodo {siguiente_nodo} (siguiendo el camino más corto hacia la llave).")
    return siguiente_nodo


def tomar_camino_al_azar(nodo_actual, nodos_llave):
    # Verificar si el héroe ya ha encontrado la llave
    if nodo_actual in nodos_llave:
        print(f"El héroe ya tiene la llave. Permanece en el nodo {nodo_actual}.")
        return nodo_actual

    # Obtener los nodos vecinos disponibles
    caminos_disponibles = grafo.get(nodo_actual, [])
    
    # Si es una bifurcación, elegir aleatoriamente sin incluir la ruta de regreso
    if len(caminos_disponibles) > 1:
        # Eliminar la ruta de regreso si existe
        caminos_disponibles_sin_retorno = [nodo for nodo in caminos_disponibles if nodo != nodo_anterior]
        
        if caminos_disponibles_sin_retorno:
            nuevo_nodo = random.choice(caminos_disponibles_sin_retorno)
        else:
            nuevo_nodo = random.choice(caminos_disponibles)
    else:
        # Si no es una bifurcación, moverse al siguiente nodo disponible
        nuevo_nodo = caminos_disponibles[0] if caminos_disponibles else nodo_actual

    print(f"El héroe se mueve al nodo {nuevo_nodo}.")

    # Verificar si el héroe está en una de las casillas posiblemente con la llave al final del movimiento
    if nuevo_nodo in nodos_llave:
        print(f"El héroe llegó a una casilla posiblemente con la llave. Verificando...")
        if random.random() < 0.5:  # Supongamos que hay un 50% de probabilidad de encontrar la llave
            print("¡El héroe encontró la llave! ¡Ha salvado a la princesa y ganó el juego!")
            return nuevo_nodo
        else:
            print("La llave no estaba aquí. El héroe se queda en esta casilla hasta el próximo lanzamiento del dado.")
            return nodo_actual
    else:
        return nuevo_nodo

while True:
    print("Nodo actual del héroe:", nodo_heroe)
    print("Nodo actual de la bruja:", nodo_bruja)

    if nodo_heroe == nodo_llave:
        print("¡El héroe encontró la llave!")
        break

    if nodo_bruja == nodo_llave:
        print("¡La bruja encontró la llave!")
        break

    dado_resultado = tirar_dado()
    movimiento_heroe, movimiento_bruja = dado_resultado

    print("Movimiento del héroe:", movimiento_heroe)
    print("Movimiento de la bruja:", movimiento_bruja)

    nodo_heroe = tomar_camino_al_azar(nodo_heroe, nodos_llave)
    nodo_anterior_heroe = nodo_heroe

    nodo_bruja = seguir_camino_bruja(nodo_bruja, nodo_llave, nodo_anterior_bruja)
    nodo_anterior_bruja = nodo_bruja

    print("El héroe se mueve al nodo", nodo_heroe)
    print("La bruja se mueve al nodo", nodo_bruja)

    print("--------------------")


