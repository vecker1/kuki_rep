import random
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation

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

# Función para mover al héroe - Sin cambios
def mover_heroe(nodo_actual, pasos, nodo_anterior):
    for _ in range(pasos):
        nuevo_nodo = mover_heroe_aleatorio(nodo_actual, nodo_anterior)
        nodo_anterior = nodo_actual  # Actualizar el nodo anterior
        nodo_actual = nuevo_nodo
    return nodo_actual

def mover_heroe_aleatorio(nodo_actual, nodo_anterior):
    caminos_disponibles = grafo.get(nodo_actual, [])

    # Excluir el nodo 4 de los posibles movimientos
    if '4' in caminos_disponibles:
        caminos_disponibles.remove('4')

    # Nueva restricción: si el héroe está en el nodo 3, no puede moverse al nodo 2
    if nodo_actual == '3' and '2' in caminos_disponibles:
        caminos_disponibles.remove('2')

    # Evitar volver al nodo anterior y asegurarse de que ningún nodo en el camino sea igual a nodo_anterior
    caminos_disponibles = [nodo for nodo in caminos_disponibles if nodo != nodo_anterior and not any(prev_node == nodo for prev_node in grafo[nodo])]

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
    return


# Función para mover a la bruja - Modificada para evitar bucles
def mover_bruja(nodo_actual, nodo_destino):
    if nodo_actual == nodo_destino:
        return nodo_actual
    camino = bfs_camino_mas_corto(grafo, nodo_actual, nodo_destino)
    if len(camino) > 1:
        return camino[1]  # Siguiente paso en el camino más corto
    else:
        # Si no hay camino disponible, moverse a un nodo vecino aleatorio
        vecinos = grafo.get(nodo_actual, [])
        return random.choice(vecinos) if vecinos else nodo_actual



#simulacion montecarlo
def realizar_simulacion(nodo_heroe_inicial, tipo_dado):
    nodo_heroe = nodo_heroe_inicial
    nodo_bruja = '8'  
    nodo_llave = random.choice(nodos_llave)
    nodo_anterior_heroe = None

        ####AQUI HAY VARIOS COMENTARIOS LOS CUALES SE PUEDE VER A PROFUNDIDAD...####
                ####LOS RESULTADOS DADOS Y MOVIMIENTOS DE HEROE Y BRUJA####

    #print(f"Inicio de la simulación - Llave en el nodo: {nodo_llave}")

    while True:

        movimiento_heroe, movimiento_bruja = tirar_dado(tipo_dado)

        #print en comentarios para ver a mas detalle los resultado de los dados
        #print(f"Resultado del dado para el Héroe: {movimiento_heroe}")
        #print(f"Resultado del dado para la Bruja: {movimiento_bruja}")

        #movimientos heroe
        nuevo_nodo_heroe = mover_heroe(nodo_heroe, movimiento_heroe, nodo_anterior_heroe)
        nodo_anterior_heroe = nodo_heroe  # Actualizar el nodo anterior del héroe antes de moverlo
        nodo_heroe = nuevo_nodo_heroe  # Mover al héroe

        #print(f"Héroe se mueve a {nodo_heroe}")  # print para ver movimiento del héroe

        #movimiento bruja
        if movimiento_bruja > 0:
            nodo_bruja = mover_bruja(nodo_bruja, nodo_llave)
            #print(f"Bruja se mueve a {nodo_bruja}")  #print para ver movimiento de la bruja
        #else :
            #print(f"Bruja se mantiene en {nodo_bruja}")  #lo mismo pero en caso de que salga 0 y no se mueva

        #print("*"*40)#separador para ver los resultados de forma ordenada


        # Condiciones de victoria
        if nodo_heroe == nodo_llave:
            #print("Héroe gana")  # Resultado de la simulación
            return "Héroe"
        if nodo_bruja == nodo_llave:
            #print("Bruja gana")  # Resultado de la simulación
            return "Bruja"


########################################################################################


cadena = "TORRE ENCANTADA".capitalize()
print(cadena.center(50, "="))
cadena = "por: Diego Cabezas y Francisco Ramírez".capitalize()
print(cadena.center(50, "="))
print("")
print("*"*49)
print("* eliga el tipo de dado:                         *")
print("* tipo [1]: dado original                       *")
print("* tipo [2]: dado con movimiento extra al heroe  *")
print("* tipo [3]: dado con movimiento extra a la bruja*")
print("*"*49)
print("Elige el tipo de dado a utilizar (1, 2, o 3):")

tipo_dado = input()
while tipo_dado not in ['1', '2', '3']:
    print("Entrada no válida. Elige el tipo de dado a utilizar (1, 2, o 3): ")
    tipo_dado = input()

while True:
    try:
        num_simulaciones = int(input("¿Cuántas simulaciones deseas realizar? "))
        if num_simulaciones >= 5000:
            break
        else:
            print("El número de simulaciones debe ser igual a 5000 o mayor. Intenta de nuevo.")
    except ValueError:
        print("Por favor, ingresa un número entero válido.")


resultados_por_nodo_inicial = {}
for nodo_inicial in ['1', '2', '3']:
    resultados = {"Héroe": 0, "Bruja": 0}
    
    for i in range(num_simulaciones):
        ganador = realizar_simulacion(nodo_inicial, tipo_dado)
        resultados[ganador] += 1

        if (i + 1) % 100 == 0: #ver si todo esta bien y no se pega en una iteracion
            print(f"***Estoy en la iteración {i + 1}***")

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