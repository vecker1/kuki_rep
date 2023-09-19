import time

def matriz_reloj(matriz):            # Función principal
    print("\nNumeros imprimidos segun el orden de la figura del taller:")
    filas = len(matriz)             
    columnas = len(matriz[0])
    
    arriba, abajo, izq, der = 0, filas - 1, 0, columnas - 1   # Definir las variables a ocupar
    
    while (arriba <= abajo and izq <= der):
        
        for col in range(izq, der + 1):  # Imprimir la fila superior
            print(matriz[arriba][col], end=' ')
        arriba += 1
        
        for filas in range(arriba, abajo + 1):  # Imprimir la columna derecha
            print(matriz[filas][der], end=' ')
        der -= 1
        
        
        if arriba <= abajo:
            for col in range(der, izq - 1, -1):  # Imprimir la fila inferior (si aún es válido hacerlo)
                print(matriz[abajo][col], end=' ')
            abajo -= 1
        
       
        if izq <= der:
            for filas in range(abajo, arriba - 1, -1):   # Imprimir la columna izquierda (si aún es válido hacerlo)
                print(matriz[filas][izq], end=' ')
            izq += 1


######################################################################


size = int(input("\nIngrese el tamaño de la matriz (mxm):\n\nm="))  # Pedir al usuario el tamaño (size) de la matriz
print("---------------------------------------------------------")

matriz = [[0] * size for _ in range(size)]    # Creacion de la matriz con el tamaño idicado por el usuario

for i in range(size):
    for j in range(size):
        matriz[i][j] = int(input(f"Guarde un número para la celda ({i}, {j}): "))   # Llenar la matriz con los números ingresados por el usuario


print("---------------------------------------------------------")
print("Matriz resultante:")  # Imprimir la matriz resultante
for fila in matriz:
    print(" ".join(map(str, fila)))

matriz_reloj(matriz)  # Funcion para imprimir la matriz
print(" ")
print("---------------------------------------------------------")

time.sleep(30)

