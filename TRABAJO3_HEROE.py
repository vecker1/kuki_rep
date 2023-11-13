import random

# Definir el grafo
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'E'],       #crear todo el mapa del taller.
    'E': ['D', 'F'],
    'F': ['E']
}

# Definir el nodo inicial y la llave
nodo_actual = 'A'
print("comienza en el nodo A!!!")
llave = 'F'

# Función para lanzar el dado y obtener la cantidad de movimientos
def lanzar_dado_heroe():
    resultado=random.randint(0, 3)
    print("El resultado del dado es:", resultado)
    return resultado

def lanzar_dado_bruja():
    resultado_bruja=random.randint(0, 2)
    print("El resultado del dado bruja es:", resultado_bruja)
    return resultado_bruja


def moverse_bruja():
    global nodo_actual
    cantidad_movimientos = lanzar_dado_bruja()
    #for _ in range(cantidad_movimientos):
        #programar ruta de la bruja

# Función para moverse al siguiente nodo de forma aleatoria
def moverse_heroe():
    global nodo_actual
    cantidad_movimientos = lanzar_dado_heroe()
    for _ in range(cantidad_movimientos):
        siguiente_nodo = random.choice(grafo[nodo_actual])
        nodo_actual = siguiente_nodo

# Simulación del recorrido hasta encontrar la llave

while nodo_actual != llave:
    moverse_heroe()
    #moverse_bruja()
    print("El aventurero se mueve al nodo:", nodo_actual)

print("¡Encontraste la llave en el nodo", nodo_actual, "! ¡Ganaste!")
