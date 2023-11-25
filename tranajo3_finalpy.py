import random
import matplotlib.pyplot as plt
import numpy as np

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
    '10': ['9', '16', '17'],
    '11': ['12', '17'],
    '12': ['11', '18'],
    '13': ['14', '20'],
    '14': ['3', '13', '22'],
    '15': ['3', '16', '23', '27'],
    '16': ['10', '15'],
    '17': ['10', '11', '27'],
    '18': ['12', '19', '28', '29'],
    '19': ['18'],
    '20': ['13', '21', '24'],
    '21': ['20', '22'],
    '22': ['14', '21', '23', '25'],
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
    '41': ['37', '40', '42'],
    '42': ['33', '38', '41']
}

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
def tirar_dado(tipo_dado):
    dado_original = [
        (3, 1),  # Cara 1: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 2: Mueve al héroe 1 y a la bruja 1
        (2, 0),  # Cara 3: Mueve al héroe 2 y a la bruja 0
        (3, 1),  # Cara 4: Mueve al héroe 3 y a la bruja 1
        (1, 1),  # Cara 5: Mueve al héroe 1 y a la bruja 1
        (0, 2)  # Cara 6: Mueve al héroe 0 y a la bruja 2
    ]
    dado_2 = [(mov_heroe + 1, mov_bruja) for mov_heroe, mov_bruja in dado_original]
    dado_3 = [(mov_heroe, mov_bruja + 1) for mov_heroe, mov_bruja in dado_original]

    if tipo_dado == '1':
        return random.choice(dado_original)
    elif tipo_dado == '2':
        return random.choice(dado_2)
    else:  # tipo_dado == '3'
        return random.choice(dado_3)


# Funciones para mover al héroe y a la bruja...
# Función para mover al héroe
def mover_heroe(nodo_actual, pasos, nodo_anterior):
    for _ in range(pasos):
        nuevo_nodo = mover_heroe_aleatorio(nodo_actual, nodo_anterior)
        nodo_anterior = nodo_actual  # Actualizar el nodo anterior
        nodo_actual = nuevo_nodo
    return nodo_actual


def mover_heroe_aleatorio(nodo_actual, nodo_anterior):
    caminos_disponibles = grafo.get(nodo_actual, [])

    # Excluir el nodo anterior de los posibles movimientos, excepto en los nodos 19 y 1
    if nodo_actual not in ['19'] and nodo_anterior in caminos_disponibles:
        caminos_disponibles.remove(nodo_anterior)

    # Excluir el nodo 4 de los posibles movimientos
    if '4' in caminos_disponibles:
        caminos_disponibles.remove('4')

    # Nueva restricción: si el héroe está en el nodo 3, no puede moverse al nodo 2
    if nodo_actual == '3' and '2' in caminos_disponibles:
        caminos_disponibles.remove('2')

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


# Modificar la función realizar_simulacion para incluir el nodo anterior
def realizar_simulacion(nodo_heroe_inicial, tipo_dado):
    nodo_heroe = nodo_heroe_inicial
    nodo_bruja = '8'  # Nodo inicial de la bruja
    nodo_llave = random.choice(nodos_llave)
    nodo_anterior_heroe = None  # Inicializar el nodo anterior del héroe

    while True:
        movimiento_heroe, movimiento_bruja = tirar_dado(tipo_dado)

        # Mover al héroe con la nueva restricción
        nuevo_nodo_heroe = mover_heroe(nodo_heroe, movimiento_heroe, nodo_anterior_heroe)
        nodo_anterior_heroe = nodo_heroe  # Actualizar el nodo anterior del héroe antes de moverlo
        nodo_heroe = nuevo_nodo_heroe  # Mover al héroe

        # Mover a la bruja
        if movimiento_bruja > 0:
            nodo_bruja = mover_bruja(nodo_bruja, nodo_llave)

        # Condiciones de victoria
        if nodo_heroe == nodo_llave:
            return "Héroe"
        if nodo_bruja == nodo_llave:
            return "Bruja"


# Realizar las simulaciones para cada tipo de dado
resultados = {}
for tipo_dado in ['1', '2', '3']:
    resultados_tipo_dado = {"Héroe": 0, "Bruja": 0}
    for _ in range(num_simulaciones):
        ganador = realizar_simulacion(nodo_heroe_inicial, tipo_dado)
        resultados_tipo_dado[ganador] += 1
    resultados[tipo_dado] = resultados_tipo_dado

# Mostrar resultados finales con porcentajes para cada tipo de dado
print(f"Resultados finales de {num_simulaciones} simulaciones para cada tipo de dado:")
for tipo_dado, resultados_tipo in resultados.items():
    porcentaje_heroe = (resultados_tipo['Héroe'] / num_simulaciones) * 100
    porcentaje_bruja = (resultados_tipo['Bruja'] / num_simulaciones) * 100
    print(f"\nDado tipo {tipo_dado}:")
    print(f"Héroe ganó {resultados_tipo['Héroe']} veces ({porcentaje_heroe:.2f}%).")
    print(f"Bruja ganó {resultados_tipo['Bruja']} veces ({porcentaje_bruja:.2f}%).")

# Preparar los datos para el gráfico
labels = ['Dado 1', 'Dado 2', 'Dado 3']
hero_wins = [resultados['1']['Héroe'], resultados['2']['Héroe'], resultados['3']['Héroe']]
witch_wins = [resultados['1']['Bruja'], resultados['2']['Bruja'], resultados['3']['Bruja']]

x = np.arange(len(labels))  # Las etiquetas de los grupos
width = 0.35  # El ancho de las barras

# Crear el gráfico
fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, hero_wins, width, label='Héroe')
rects2 = ax.bar(x + width / 2, witch_wins, width, label='Bruja')

# Añadir algunas características al gráfico
ax.set_xlabel('Tipo de Dado')
ax.set_ylabel('Victorias')
ax.set_title('Victorias por tipo de dado y competidor')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


# Función para añadir etiquetas a las barras
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # Desplazamiento vertical de la etiqueta
                    textcoords="offset points",
                    ha='center', va='bottom')


# Llamar a la función para cada grupo de barras
autolabel(rects1)
autolabel(rects2)

plt.show()
