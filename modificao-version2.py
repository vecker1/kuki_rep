import random
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
#pip install scipy

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

def mover_heroe(nodo_actual, nodo_anterior_heroe, nodo_llave):
    caminos_disponibles = grafo.get(nodo_actual, [])

    # Excluir el nodo anterior del héroe de los posibles movimientos
    if nodo_anterior_heroe in caminos_disponibles:
        caminos_disponibles.remove(nodo_anterior_heroe)

    # Restricción: no pasar por nodos (1, 2, 3, 4, 5, 6, 7, 8) al pasar por el nodo 3
    if nodo_actual == '3':
        caminos_disponibles = [nodo for nodo in caminos_disponibles if nodo not in {'1', '2', '4', '5', '6', '7', '8'}]

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

def mover_bruja(nodo_actual_bruja, nodo_llave):
    movimiento_bruja = tirar_dado('3')[1]  # Utilizar la segunda componente del dado tipo 3

    # Restricción: no pasar por nodos (1, 2, 3, 4, 5, 6, 7, 8) al pasar por el nodo 3
    if nodo_actual_bruja == '3':
        return nodo_actual_bruja

    # Si la bruja está en el mismo nodo que la llave, no se mueve
    if nodo_actual_bruja == nodo_llave:
        return nodo_actual_bruja

    # Calcular el camino más corto hacia la llave
    camino = bfs_camino_mas_corto(grafo, nodo_actual_bruja, nodo_llave)

    # Si hay un camino disponible, avanzar hacia la llave
    if len(camino) > 1:
        siguiente_paso = camino[1]
        return siguiente_paso

    return nodo_actual_bruja  # Si no hay camino disponible, no se mueve



def realizar_simulacion(nodo_heroe_inicial, tipo_dado):
    nodo_heroe = nodo_heroe_inicial
    nodo_bruja = '8'  # Nodo inicial de la bruja
    nodo_llave = random.choice(nodos_llave)
    nodo_anterior_heroe = None  # Inicializar el nodo anterior del héroe

    print(f"Inicio de la simulación - Llave en el nodo: {nodo_llave}")  # Mostrar ubicación de la llave

    while True:
        # Mover al héroe con la nueva restricción
        nuevo_nodo_heroe = mover_heroe(nodo_heroe, nodo_anterior_heroe, nodo_llave)
        nodo_anterior_heroe = nodo_heroe  # Actualizar el nodo anterior del héroe antes de moverlo
        nodo_heroe = nuevo_nodo_heroe  # Mover al héroe

        print(f"Héroe se mueve a {nodo_heroe}")  # Seguimiento del movimiento del héroe

        # Mover a la bruja
        nodo_bruja = mover_bruja(nodo_bruja, nodo_llave)
        print(f"Bruja se mueve a {nodo_bruja}")  # Seguimiento del movimiento de la bruja

        # Condiciones de victoria
        if nodo_heroe == nodo_llave:
            print("Héroe gana")  # Resultado de la simulación
            return "Héroe"
        if nodo_bruja == nodo_llave:
            print("Bruja gana")  # Resultado de la simulación
            return "Bruja"




# Preguntar al usuario qué tipo de dado usar
print("*"*49)
print("* tipo [1]: dado original                       *")
print("* tipo [2]: dado con movimiento extra al heroe  *")
print("* tipo [3]: dado con movimiento extra a la bruja*")
print("*"*49)
print("Elige el tipo de dado a utilizar (1, 2, o 3):")

tipo_dado = input()
while tipo_dado not in ['1', '2', '3']:
    print("Entrada no válida. Elige el tipo de dado a utilizar (1, 2, o 3): ")
    tipo_dado = input()

# Preguntar al usuario cuántas simulaciones realizar
print("¿Cuántas simulaciones deseas realizar?")
num_simulaciones = int(input())

# Realizar las simulaciones para cada nodo inicial del héroe
resultados_por_nodo_inicial = {}
for nodo_inicial in ['1', '2', '3']:
    resultados = {"Héroe": 0, "Bruja": 0}
    for _ in range(num_simulaciones):
        ganador = realizar_simulacion(nodo_inicial, tipo_dado)
        resultados[ganador] += 1
    resultados_por_nodo_inicial[nodo_inicial] = resultados

# Mostrar resultados finales
print(f"Resultados de {num_simulaciones} simulaciones para el dado tipo {tipo_dado}:")
for nodo_inicial, resultados in resultados_por_nodo_inicial.items():
    porcentaje_heroe = (resultados['Héroe'] / num_simulaciones) * 100
    porcentaje_bruja = (resultados['Bruja'] / num_simulaciones) * 100
    print(f"\nNodo inicial del héroe: {nodo_inicial}")
    print(f"Héroe ganó {resultados['Héroe']} veces ({porcentaje_heroe:.2f}%).")
    print(f"Bruja ganó {resultados['Bruja']} veces ({porcentaje_bruja:.2f}%).")

# Preparar los datos para el gráfico
nodos_iniciales = ['1', '2', '3']
victorias_heroe = [resultados_por_nodo_inicial[nodo]['Héroe'] for nodo in nodos_iniciales]
victorias_bruja = [resultados_por_nodo_inicial[nodo]['Bruja'] for nodo in nodos_iniciales]


##VENTANA CON EL GRAFICO##

x = np.arange(len(nodos_iniciales))  # Las etiquetas de los grupos
width = 0.35  # El ancho de las barras

# Crear el gráfico
fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, victorias_heroe, width, label='Héroe')
rects2 = ax.bar(x + width / 2, victorias_bruja, width, label='Bruja')

# Añadir algunas características al gráfico
ax.set_xlabel('Nodo Inicial del Héroe')
ax.set_ylabel('Victorias')
ax.set_title('Victorias por nodo inicial del héroe y competidor')
ax.set_xticks(x)
ax.set_xticklabels(nodos_iniciales)
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

##VENTANA CON EL GRAFO##

# Crear un objeto de grafo no dirigido
G = nx.Graph(grafo)

# Dibujar el grafo con disposición de Kamada-Kawai
pos = nx.kamada_kawai_layout(G)

# Crear un diccionario de colores para nodos
node_colors = {
    '19': '#99F58F',     #color llave1
    '38': '#99F58F',     #color llave2
    '41': '#99F58F',     #color llave3
    '1': '#82BEF3',     #color posicion heroe1
    '2': '#82BEF3',     #color posicion heroe2
    '3': '#82BEF3',     #color posicion heroe3
    '8': '#DABDF5',      #color posicion bruja
}

# Obtener una lista de colores según los nodos
colors = [node_colors[node] if node in node_colors else '#F9D8B7' for node in G.nodes()]        #tamaño y color nodos

# Configurar el color de fondo
fig = plt.figure(facecolor='blue')

# Dibujar nodos
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=300, node_color=colors, font_size=8)

# Dibujar aristas
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='gray')



# Agregar texto
plt.text(pos['19'][0], pos['19'][1] + 0.05, 'Llave 1', color='red', fontsize=8, ha='center')
plt.text(pos['38'][0], pos['38'][1] + 0.05, 'Llave 2', color='red', fontsize=8, ha='center')
plt.text(pos['41'][0], pos['41'][1] + 0.05, 'Llave 3', color='red', fontsize=8, ha='center')
plt.text(pos['1'][0], pos['1'][1] + 0.05, 'Heroe pos.1', color='green', fontsize=8, ha='center')
plt.text(pos['2'][0], pos['2'][1] + 0.05, 'Heore pos.2', color='green', fontsize=8, ha='center')
plt.text(pos['3'][0], pos['3'][1] + 0.05, 'Heroe pos.3', color='green', fontsize=8, ha='center')
plt.text(pos['8'][0], pos['8'][1] + 0.05, 'Bruja', color='black', fontsize=8, ha='center')


plt.show()
