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

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

##########################################################################################

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

    return C[0][n - 1], '-'.join(partitions)

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

    return C[n - 1], '-'.join(partitions)

#############################################################################################################

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
    current_random_string = None  # Utiliza un nombre diferente para evitar confusiones
    firsttime = 0
    results_recursive = []
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    results_dp = []
    generated_strings = []
    random_str = None

    while True:
        if firsttime == 0:
            print("=======================================================================================   /\__/\ ")
            print("| Trabajo 2 - Algoritmos y Programación                                               |   (='.'=)") 
            print("| Integrante: Diego Cabezas ||| Sección: 411 ||| Profesor: Luis Hernan Herrera Becerra|   ('')_('')")
            print("=======================================================================================")
            jump_line()
        print("Menú de opciones:")
        void()
        print("1. Resolver el problema de partición de palíndromos con ambos algoritmos")
        print("2. Generar gráficos comparando el tiempo y memoria de ejecución [100-1000]")
        print("3. Salir")
        jump_line()
        option = input("Seleccione una opción: ")
        jump_line()

        if option == "1":
            x=0
            try:
                firsttime = 1
                print("Eliga como resolver el problema de partición de palíndromos:")
                void()
                print("1. Ingresar un tamaño de caracteres y generar una cadena aletoria")
                print("2. Generar automaticamente varias cadenas aletorias de [100 a 1000] caracteres")
                void()
                print("Nota: Cada vez que se genere una cadena, esta se reemplazará por la anterior.")
                void()
                option_2 = input("Seleccione una opción: ")
                if option_2 == "1":
                    ################################################################################################
                    jump_line()
                    length = int(input("¿De cuantos caracteres quieres que sea la cadena?: "))
                    random_string = generate_random_string(length)
                    with open("cadena_opcion_1.txt", "w") as file:
                        file.write(random_string)
                    jump_line()
                    print(f"Cadena generada con éxito y guardada en [cadena_opcion_1.txt]")
                    firsttime = 1
                    jump_line()
                    ###############################################################################################
                    start_time = time.time()
                    cuts_recursive, partition_recursive = min_palindrome_cuts_recursive(random_string)
                    results_recursive.append(time.time() - start_time)
                    print(f"Algoritmo O(n^3) -> Mínimo de cortes: {cuts_recursive}")
                    void()
                    print(f"Cadena con los cortes: {partition_recursive}")
                    jump_line()

                    start_time = time.time()
                    cuts_dp, partition_dp = min_palindrome_cuts_dp(random_string)
                    results_dp.append(time.time() - start_time)
                    print(f"Algoritmo O(n^2) -> Mínimo de cortes: {cuts_dp}")
                    void()
                    print(f"Cadena con los cortes: {partition_dp}")
                    jump_line()

                    # Imprimir resultados de tiempos
                    print("\nTiempos de ejecución del algoritmo (O(n^3)):", results_recursive)
                    print("Tiempos de ejecución del algoritmo (O(n^2)):", results_dp)
                    void()
                    save_path = "execution_times_option_1.txt"
                    with open(save_path, "w") as file:
                        file.write(f"Tiempo de ejecucion del algoritmo O(n^3): {results_recursive} segundos\n")
                        file.write(f"Tiempo de ejecucion del algoritmo O(n^2): {results_dp} segundos\n")
                    print(f"Tiempos de ejecución guardados en la carpeta local llamado [{save_path}]")
                    jump_line()
                    ################################################################################################
                elif option_2 == "2":
                    # Generar y guardar las cadenas generadas
                    for size in sizes:
                        s = generate_random_string(size)  # Use generate_random_string instead of random_string
                        generated_strings.append(s)

                    with open('cadenas_opcion_2.txt', 'w') as f:
                        for s in generated_strings:
                            f.write(s + '\n')
                    n=0
                    i=0
                    for s in generated_strings:
                        size = len(s)
                        print(f"\nCadena generada (tamaño {size}): {s}")
                        
                        start_time = time.time()
                        cuts_recursive, partition_recursive = min_palindrome_cuts_recursive(s)
                        results_recursive.append(time.time() - start_time)
                        print(f"Algoritmo O(n^3) -> Mínimo de cortes: {cuts_recursive}")
                        void()
                        print(f"Cadena con los cortes: {partition_recursive} \n \n con tiempo de ejecución: {results_recursive[i]} segundos")
                        i=i+1
                        jump_line()
                        start_time = time.time()
                        cuts_dp, partition_dp = min_palindrome_cuts_dp(s)
                        results_dp.append(time.time() - start_time)
                        print(f"Algoritmo O(n^2) -> Mínimo de cortes: {cuts_dp}")
                        void()
                        print(f"Cadena con los cortes: {partition_dp} \n \nCon tiempo de ejecución: {results_dp[n]} segundos")
                        n=n+1
                        jump_line()

                    # Imprimir resultados de tiempos
                    jump_line()
                    print("Tiempos ordenados de 100 a 1000:")
                    void()
                    print(f"\nTiempos de ejecución del algoritmo (O(n^3)): {results_recursive}")
                    void()
                    print(f"Tiempos de ejecución del algoritmo (O(n^2)): {results_dp}")
                    jump_line()
                    save_path = "execution_times_option_2.txt"
                    with open(save_path, "w") as file:
                        file.write("Tiempos ordenados de 100 a 1000:")
                        file.write(" ")
                        file.write(f"Tiempo de ejecucion del algoritmo O(n^3): {results_recursive} segundos\n")
                        file.write(f"Tiempo de ejecucion del algoritmo O(n^2): {results_dp} segundos\n")
                    print(f"Tiempos de ejecución guardados en la carpeta local llamado [{save_path}]")
                    jump_line()
                ###################################################################


                jump_line()
            except FileNotFoundError:
                print("====================================================================================================")
                jump_line()


        elif option == "2":
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
        
        elif option == "3":
            break
        
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
            jump_line()

if __name__ == "__main__":
    main()
