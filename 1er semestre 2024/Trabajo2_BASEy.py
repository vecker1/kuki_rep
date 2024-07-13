import random
import string
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

def void():
    print("")

def jump_line():
    print("_________________________________________________________________________________________")
    void()

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def palindrome_partitioning_min_cuts(str):
    n = len(str)
    C = [[0 for i in range(n)] for j in range(n)]
    P = [[False for i in range(n)] for j in range(n)]

    for i in range(n):
        P[i][i] = True
        C[i][i] = 0

    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if L == 2:
                P[i][j] = (str[i] == str[j])
            else:
                P[i][j] = (str[i] == str[j]) and P[i + 1][j - 1]
            if P[i][j]:
                C[i][j] = 0
            else:
                C[i][j] = float('inf')
                for k in range(i, j):
                    if C[i][j] > C[i][k] + C[k + 1][j] + 1:
                        C[i][j] = C[i][k] + C[k + 1][j] + 1
    return C, P

def construct_solution(C, P, str):
    n = len(str)
    result = []
    cuts = []

    def add_cuts(i, j):
        if i >= j or P[i][j]:
            result.append(str[i:j+1])
            return
        for k in range(i, j):
            if C[i][j] == C[i][k] + C[k + 1][j] + 1:
                cuts.append(k + 1)
                add_cuts(i, k)
                add_cuts(k + 1, j)
                break
    
    add_cuts(0, n - 1)
    return '-'.join(result), len(cuts)

def dynamic_programming_palindrome_partitioning(s):
    n = len(s)
    cuts = [0 for _ in range(n)]
    pal = [[False for _ in range(n)] for _ in range(n)]

    for i in range(n):
        min_cut = i
        for j in range(i + 1):
            if s[i] == s[j] and (i - j < 2 or pal[j + 1][i - 1]):
                pal[j][i] = True
                min_cut = 0 if j == 0 else min(min_cut, cuts[j - 1] + 1)
        cuts[i] = min_cut

    return cuts[-1], pal


def construct_solution_dp(cuts, pal, str):
    n = len(str)
    result = []
    i = n - 1

    while i >= 0:
        j = i
        while j >= 0 and not pal[j][i]:
            j -= 1
        result.append(str[j:i+1])
        i = j - 1

    return '-'.join(result[::-1]), len(result) - 1

def measure_execution_time(func, str):
    start_time = time.time()
    result = func(str)
    end_time = time.time()
    return end_time - start_time, result

def measure_all(length):
    random_string = generate_random_string(length)
    time1, _ = measure_execution_time(lambda s: construct_solution(*palindrome_partitioning_min_cuts(s), s), random_string)
    time2, _ = measure_execution_time(lambda s: construct_solution_dp(*dynamic_programming_palindrome_partitioning(s), s), random_string)
    return (time1, time2)

def main():
    random_string = None
    firsttime = 0
    
    while True:
        if firsttime == 0:
            print("=======================================================================================   (\__/)")
            print("| Trabajo 2 - Algoritmos y Programación                                               |   (='.'=)") 
            print("| Integrante: Diego Cabezas ||| Sección: 411 ||| Profesor: Luis Hernan Herrera Becerra |   ('')_('')")
            print("=======================================================================================")
            jump_line()
        print("Menú de opciones:")
        void()
        print("1. Generar o re-generar .txt con una cadena de caracteres aleatoria")
        if firsttime == 0:
            void()
            print("================================================================")
            print("| Te recomendamos ingresar a la primera opción primero         |")
            print("| para que el programa pueda resolver las siguientes opciones. |")
            print("================================================================")
            void()
        print("2. Resolver el problema de partición de palíndromos con ambos algoritmos")
        print("3. Medir el tiempo de ejecución de cada algoritmo")
        print("4. Analizar la complejidad computacional de cada algoritmo")
        print("5. Generar gráficos comparando el tiempo de ejecución")
        print("6. Salir")
        jump_line()
        option = input("Seleccione una opción: ")

        if option == "1":
            jump_line()
            length = int(input("Ingrese la longitud de la cadena: "))
            random_string = generate_random_string(length)
            with open("cadena.txt", "w") as file:
                file.write(random_string)
            jump_line()
            print(f"Cadena generada con éxito y guardada en cadena.txt")
            firsttime = 1
            jump_line()

        elif option == "2":
            try:
                with open("cadena.txt", "r") as file:
                    random_string = file.read()
                C, P = palindrome_partitioning_min_cuts(random_string)
                solution1, cuts1 = construct_solution(C, P, random_string)
                cuts2, pal = dynamic_programming_palindrome_partitioning(random_string)
                solution2, _ = construct_solution_dp(cuts2, pal, random_string)
                print(f"Resultado del algoritmo O(n^3): {solution1} con {cuts1} cortes")
                void()
                print(f"Resultado del algoritmo O(n^2): {solution2} con {cuts2} cortes")
                jump_line()
            except FileNotFoundError:
                print("Primero debe generar una cadena aleatoria en la opción 1.")
                jump_line()

        elif option == "3":
            try:
                with open("cadena.txt", "r") as file:
                    random_string = file.read()
                time1, _ = measure_execution_time(lambda s: construct_solution(*palindrome_partitioning_min_cuts(s), s), random_string)
                time2, _ = measure_execution_time(lambda s: construct_solution_dp(*dynamic_programming_palindrome_partitioning(s), s), random_string)
                print(f"Tiempo de ejecución del algoritmo O(n^3): {time1} segundos")
                print(f"Tiempo de ejecución del algoritmo O(n^2): {time2} segundos")
                save_path = "execution_times.txt"
                with open(save_path, "w") as file:
                    file.write(f"Tiempo de ejecución del algoritmo O(n^3): {time1} segundos\n")
                    file.write(f"Tiempo de ejecución del algoritmo O(n^2): {time2} segundos\n")
                print(f"Tiempos de ejecución guardados en {save_path}")
            except FileNotFoundError:
                print("Primero debe generar una cadena aleatoria en la opción 1.")
                jump_line()

        elif option == "4":
            print("Complejidad computacional:")
            print("Algoritmo O(n^3):")
            print("El algoritmo O(n^3) tiene una complejidad cúbica debido a los tres bucles anidados. La formación de la matriz de palíndromos toma O(n^2) y calcular los cortes mínimos toma O(n^3).")
            print("Algoritmo O(n^2):")
            print("El algoritmo O(n^2) mejora la eficiencia utilizando programación dinámica. La complejidad es O(n^2) debido a la matriz de palíndromos y la búsqueda del mínimo número de cortes.")
            print("\nExplicación matemática:")
            print("Para el algoritmo O(n^3):")
            print("El bucle exterior itera n veces, el siguiente bucle itera n veces y el último bucle también itera n veces en el peor de los casos. Por lo tanto, la complejidad es O(n * n * n) = O(n^3).")
            print("Para el algoritmo O(n^2):")
            print("El bucle exterior itera n veces y el bucle interior itera n veces, lo que resulta en una complejidad de O(n * n) = O(n^2).")

        elif option == "5":
            lengths = list(range(100, 1100, 100))
            times1 = []
            times2 = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(measure_all, length): length for length in lengths}
                for future in as_completed(futures):
                    length = futures[future]
                    try:
                        time1, time2 = future.result()
                        times1.append(time1)
                        times2.append(time2)
                    except Exception as exc:
                        print(f'Error al medir {length}: {exc}')

            plt.figure(figsize=(12, 6))

            plt.plot(lengths, times1, label='O(n^3)')
            plt.plot(lengths, times2, label='O(n^2)')
            plt.xlabel('Tamaño de la cadena')
            plt.ylabel('Tiempo de ejecución (segundos)')
            plt.title('Comparación de rendimiento de los algoritmos')
            plt.legend()

            plt.tight_layout()
            plt.show()
            jump_line()
        
        elif option == "6":
            break
        
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
            jump_line()

if __name__ == "__main__":
    main()
