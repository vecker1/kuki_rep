import random

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
# Definir el nodo donde se encuentra la llave
nodos_llave = ['19', '38', '41']

nodo_llave = random.choice(nodos_llave)

print("Elige el nodo inicial del héroe (1, 2, o 3):")
nodo_heroe = input()
while nodo_heroe not in ['1', '2', '3']:
    print("Entrada no válida. Elige el nodo inicial del héroe (1, 2, o 3): ")
    nodo_heroe = input()

nodo_bruja = '8'

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

# Función para que el héroe tome caminos al azar
def tomar_camino_al_azar(nodo_actual):
    caminos_disponibles = grafo.get(nodo_actual, [])
    if caminos_disponibles:
        return random.choice(caminos_disponibles)
    else:
        print(f"No hay caminos disponibles desde el nodo {nodo_actual}. El héroe se queda en el mismo nodo.")
        return nodo_actual

# Función para que la bruja siga su camino
def seguir_camino_bruja(nodo_actual):
    caminos_disponibles = grafo.get(nodo_actual, [])
    if caminos_disponibles:
        return random.choice(caminos_disponibles)
    else:
        print(f"No hay caminos disponibles desde el nodo {nodo_actual}. La bruja se queda en el mismo nodo.")
        return nodo_actual


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

    nodo_heroe = tomar_camino_al_azar(nodo_heroe) if movimiento_heroe > 0 else nodo_heroe
    nodo_bruja = seguir_camino_bruja(nodo_bruja) if movimiento_bruja > 0 else nodo_bruja

    print("El héroe se mueve al nodo", nodo_heroe)
    print("La bruja se mueve al nodo", nodo_bruja)

    print("--------------------")