import random
import string
import time
import tracemalloc
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

def dynamic_programming_palindrome_partitioning(str):
    n = len(str)
    cuts = [0 for _ in range(n)]
    pal = [[False for _ in range(n)] for _ in range(n)]

    for i in range(n):
        min_cut = i
        for j in range(i + 1):
            if str[i] == str[j] and (i - j < 2 or pal[j + 1][i - 1]):
                pal[j][i] = True
                min_cut = 0 if j == 0 else min(min_cut, cuts[j - 1] + 1)
        cuts[i] = min_cut

    result = []
    i = n - 1
    while i >= 0:
        j = i
        while j >= 0 and not pal[j][i]:
            j -= 1
        result.append(str[j:i+1])
        i = j - 1

    return '-'.join(result[::-1]), cuts[-1]

def measure_execution_time(func, str):
    start_time = time.time()
    result = func(str)
    end_time = time.time()
    return end_time - start_time, result

def measure_memory_usage(func, str):
    tracemalloc.start()
    result = func(str)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak, result

def measure_all(length):
    random_string = generate_random_string(length)
    time1, _ = measure_execution_time(palindrome_partitioning_min_cuts, random_string)
    time2, _ = measure_execution_time(dynamic_programming_palindrome_partitioning, random_string)
    memory1, _ = measure_memory_usage(palindrome_partitioning_min_cuts, random_string)
    memory2, _ = measure_memory_usage(dynamic_programming_palindrome_partitioning, random_string)
    return (time1, time2, memory1 / 1024, memory2 / 1024)  # Convert to KB

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
        print("1. Generar o re-generar una cadena de caracteres aleatoria")
        if firsttime == 0:
            print("================================================================")
            print("| Te recomendamos ingresar a la primera opción primero         |")
            print("| para que el programa pueda resolver las siguientes opciones. |")
            print("================================================================")
            void()
        print("2. Resolver el problema 0.0.1 y 0.0.2")
        print("3. Medir el tiempo de ejecución de cada algoritmo")
        print("4. Analizar la complejidad computacional de cada algoritmo")
        print("5. Graficar el rendimiento de los algoritmos [1min. de espera promedio]")
        print("6. Salir")
        jump_line()
        option = input("Seleccione una opción: ")

        if option == "1":
            jump_line()
            length = int(input("Ingrese la longitud de la cadena: "))
            random_string = generate_random_string(length)
            jump_line()
            jump_line()
            print(f"Cadena generada con éxito: {random_string}")
            firsttime = 1
            jump_line()

        elif option == "2":
            if random_string is None:
                print("Primero debe generar una cadena aleatoria.")
                jump_line()
            else:
                C, P = palindrome_partitioning_min_cuts(random_string)
                solution1, _ = construct_solution(C, P, random_string)
                solution2, _ = dynamic_programming_palindrome_partitioning(random_string)
                cuts1 = solution1.count('-')
                cuts2 = solution2.count('-')
                print(f"Resultado del algoritmo O(n^3): {solution1} con {cuts1} cortes")
                void()
                print(f"Resultado del algoritmo O(n^2): {solution2} con {cuts2} cortes")
                jump_line()

        elif option == "3":
            if random_string is None:
                print("Primero debe generar una cadena aleatoria.")
            else:
                time1, _ = measure_execution_time(palindrome_partitioning_min_cuts, random_string)
                time2, _ = measure_execution_time(dynamic_programming_palindrome_partitioning, random_string)
                print(f"Tiempo de ejecución del algoritmo O(n^3): {time1} segundos")
                print(f"Tiempo de ejecución del algoritmo O(n^2): {time2} segundos")
                save_path = "execution_times.txt"
                file = open (save_path, "w")
                file.write(f"Tiempo de ejecución del algoritmo O(n^3): {time1} segundos\n")
                file.write(f"Tiempo de ejecución del algoritmo O(n^2): {time2} segundos\n")
                file.close()
                print(f"Tiempos de ejecución guardados en {save_path}")

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
            lengths = [100, 200, 300, 400, 500,]
            times1 = []
            times2 = []
            memories1 = []
            memories2 = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = {executor.submit(measure_all, length): length for length in lengths}
                for future in as_completed(futures):
                    length = futures[future]
                    try:
                        time1, time2, memory1, memory2 = future.result()
                        times1.append(time1)
                        times2.append(time2)
                        memories1.append(memory1)
                        memories2.append(memory2)
                    except Exception as exc:
                        print(f'Error al medir {length}: {exc}')

            plt.figure(figsize=(12, 6))

            plt.subplot(1, 2, 1)
            plt.plot(lengths, times1, label='O(n^3)')
            plt.plot(lengths, times2, label='O(n^2)')
            plt.xlabel('Tamaño de la cadena')
            plt.ylabel('Tiempo de ejecución (segundos)')
            plt.title('Comparación de rendimiento de los algoritmos')
            plt.legend()

            plt.subplot(1, 2, 2)
            plt.plot(lengths, memories1, label='O(n^3)')
            plt.plot(lengths, memories2, label='O(n^2)')
            plt.xlabel('Tamaño de la cadena')
            plt.ylabel('Uso de memoria (KB)')
            plt.title('Comparación de uso de memoria de los algoritmos')
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
