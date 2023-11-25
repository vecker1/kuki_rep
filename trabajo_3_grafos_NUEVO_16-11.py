import random
import matplotlib.pyplot as plt
import networkx as nx

# Definir el grafo con los caminos
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
    '20': ['13', '21', '24'],
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

# Crear un objeto de grafo dirigido
G = nx.Graph(grafo)

# Dibujar el grafo
pos = nx.spring_layout(G)  # Colocar los nodos utilizando un algoritmo de disposición
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)

# Dibujar arcos
nx.draw_networkx_edges(G, pos, edgelist=grafo.edges(), width=1.0, alpha=0.5, edge_color='gray')

# Mostrar el grafo
plt.show()

# Definir el nodo donde se encuentra la llave
nodos_llave = ['19', '38', '41']

# Seleccionar el nodo inicial del héroe
print("Elige el nodo inicial del héroe (1, 2, o 3):")
nodo_heroe_inicial = input()
while nodo_heroe_inicial not in ['1', '2', '3']:
    print("Entrada no válida. Elige el nodo inicial del héroe (1, 2, o 3): ")
    nodo_heroe_inicial = input()

# Preguntar al usuario cuántas simulaciones realizar
print("¿Cuántas simulaciones deseas realizar?")
num_simulaciones = int(input())

# Función para tirar el dado

def tirar_dado():
    caras = [
        (3, 1),  # Cara 1: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 2: Mueve al héroe 1 y a la bruja 1
        (2, 0),  # Cara 3: Mueve al héroe 2 y a la bruja 0
        (3, 1),  # Cara 4: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 5: Mueve al héroe 1 y a la bruja 1
        (0, 2)   # Cara 6: Mueve al héroe 0 y a la bruja 2
    ]
    return random.choice(caras)

# Funciones para mover al héroe y a la bruja...
# Función para mover al héroe
def mover_heroe(nodo_actual, pasos):
    for _ in range(pasos):
        nodo_actual = mover_heroe_aleatorio(nodo_actual)
    return nodo_actual

def mover_heroe_aleatorio(nodo_actual):
    caminos_disponibles = grafo.get(nodo_actual, [])
    if caminos_disponibles:
        return random.choice(caminos_disponibles)
    return nodo_actual

# Función para realizar una búsqueda en amplitud (BFS) y encontrar el camino más corto
def bfs_camino_mas_corto(grafo, inicio, objetivo):
    cola = [(inicio, [inicio])]
    visitados = set()
    while cola:
        (nodo_actual, camino) = cola.pop(0)
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            if nodo_actual == objetivo:
                return camino
            for vecino in grafo[nodo_actual]:
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))
    return []

# Función para mover a la bruja
def mover_bruja(nodo_actual, nodo_destino):
    camino = bfs_camino_mas_corto(grafo, nodo_actual, nodo_destino)
    # Devuelve el siguiente paso en el camino más corto
    return camino[1] if len(camino) > 1 else nodo_actual
def realizar_simulacion():
    nodo_heroe = nodo_heroe_inicial
    nodo_bruja = '8'  # Nodo inicial de la bruja
    nodo_llave = random.choice(nodos_llave)

    while True:
        movimiento_heroe, movimiento_bruja = tirar_dado()

        # Mover al héroe...
        nodo_heroe = mover_heroe(nodo_heroe, movimiento_heroe)

        # Mover a la bruja
        if movimiento_bruja > 0:
            nodo_bruja = mover_bruja(nodo_bruja, nodo_llave)

        # Condiciones de victoria
        if nodo_heroe == nodo_llave:
            return "Héroe"
        if nodo_bruja == nodo_llave:
            return "Bruja"

# Realizar las simulaciones
resultados = {"Héroe": 0, "Bruja": 0}
for _ in range(num_simulaciones):
    ganador = realizar_simulacion()
    resultados[ganador] += 1

# Calcular porcentajes
porcentaje_heroe = (resultados['Héroe'] / num_simulaciones) * 100
porcentaje_bruja = (resultados['Bruja'] / num_simulaciones) * 100

# Mostrar resultados finales con porcentajes
print(f"Resultados finales de {num_simulaciones} simulaciones:")
print(f"Héroe ganó {resultados['Héroe']} veces ({porcentaje_heroe:.2f}%).")
print(f"Bruja ganó {resultados['Bruja']} veces ({porcentaje_bruja:.2f}%).")

# Crear y mostrar la gráfica automáticamente
etiquetas = ['Héroe', 'Bruja']
victorias = [resultados['Héroe'], resultados['Bruja']]
plt.bar(etiquetas, victorias, color=['blue', 'red'])
plt.xlabel('Competidor')
plt.ylabel('Número de Victorias')
plt.title('Comparación de Victorias: Héroe vs Bruja')
plt.show()
