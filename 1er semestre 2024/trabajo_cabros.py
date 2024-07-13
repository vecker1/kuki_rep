import time
import random
import string
import matplotlib.pyplot as plt
import numpy as np

# Función para generar una cadena aleatoria
def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Algoritmo A: Enfoque recursivo optimizado con memoización
def min_palindrome_cuts_recursive(s):
    n = len(s)
    C = [[0 for _ in range(n)] for _ in range(n)]
    P = [[False for _ in range(n)] for _ in range(n)]

    for i in range(n):
        P[i][i] = True

    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if L == 2:
                P[i][j] = (s[i] == s[j])
            else:
                P[i][j] = (s[i] == s[j]) and P[i + 1][j - 1]

    for i in range(n):
        if P[0][i]:
            C[0][i] = 0
        else:
            C[0][i] = float('inf')
            for j in range(i):
                if P[j + 1][i] and 1 + C[0][j] < C[0][i]:
                    C[0][i] = 1 + C[0][j]

    partitions = []
    start = 0
    while start < n:
        for end in range(n - 1, start - 1, -1):
            if P[start][end]:
                partitions.append(s[start:end + 1])
                start = end + 1
                break

    return C[0][n - 1], ' - '.join(partitions)

# Algoritmo B: Programación dinámica
def min_palindrome_cuts_dp(s):
    n = len(s)
    C = [0] * n
    P = [[False] * n for _ in range(n)]

    for i in range(n):
        P[i][i] = True

    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if L == 2:
                P[i][j] = (s[i] == s[j])
            else:
                P[i][j] = (s[i] == s[j]) and P[i + 1][j - 1]

    for i in range(n):
        if P[0][i]:
            C[i] = 0
        else:
            C[i] = float('inf')
            for j in range(i):
                if P[j + 1][i] and C[j] + 1 < C[i]:
                    C[i] = C[j] + 1

    partitions = []
    start = 0
    while start < n:
        for end in range(n - 1, start - 1, -1):
            if P[start][end]:
                partitions.append(s[start:end + 1])
                start = end + 1
                break

    return C[n - 1], ' - '.join(partitions)

# Tamaños de cadenas para pruebas
sizes = [100, 200, 300, 400, 500]  # He reducido los tamaños para facilitar la visualización
results_recursive = []
results_dp = []
generated_strings = []

# Generar y guardar las cadenas generadas
for size in sizes:
    s = random_string(size)
    generated_strings.append(s)

with open('cadenas.txt', 'w') as f:
    for s in generated_strings:
        f.write(s + '\n')

# Medir tiempos de ejecución y mostrar cadenas generadas y cortes
for s in generated_strings:
    size = len(s)
    print(f"\nCadena generada (tamaño {size}): {s}")

    start_time = time.time()
    cuts_recursive, partition_recursive = min_palindrome_cuts_recursive(s)
    results_recursive.append(time.time() - start_time)
    print(f"Recursivo - Mínimo de cortes: {cuts_recursive}")
    print(f"Partición: {partition_recursive}")

    start_time = time.time()
    cuts_dp, partition_dp = min_palindrome_cuts_dp(s)
    results_dp.append(time.time() - start_time)
    print(f"DP - Mínimo de cortes: {cuts_dp}")
    print(f"Partición: {partition_dp}")

# Imprimir resultados de tiempos
print("\nTiempos de ejecución (recursivo):", results_recursive)
print("Tiempos de ejecución (DP):", results_dp)

# Graficar resultados en un gráfico de barras
bar_width = 0.35
index = np.arange(len(sizes))

fig, ax = plt.subplots()
bar1 = ax.bar(index, results_recursive, bar_width, label='Recursivo')
bar2 = ax.bar(index + bar_width, results_dp, bar_width, label='DP')

ax.set_xlabel('Tamaño de la cadena')
ax.set_ylabel('Tiempo de ejecución (s)')
ax.set_title('Comparación de algoritmos de particionamiento de palíndromos')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(sizes)
ax.legend()

plt.show()
