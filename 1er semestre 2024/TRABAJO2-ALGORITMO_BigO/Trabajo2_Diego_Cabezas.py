import random
import string
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from memory_profiler import memory_usage #pip install memory_profiler
import psutil #pip install psutil


##########################################################################################

def void():
    print("")                                                                               #funciones esteticas

def jump_line():
    print("_________________________________________________________________________________________")
    
##########################################################################################

def generate_random_string_one(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))                         #funciones para generar cadenas aleatorias

def generate_random_string_multi(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

##########################################################################################

#Algoritmo (O(n^3)): Algoritmo A
def palindrome_cuts_A(s):
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

#Algoritmo (O(n^2)): B
def palindrome_cuts_B(s):
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

def measure_execution_time(func, str):
    start_time = time.time()
    result = func(str)
    end_time = time.time()
    return end_time - start_time, result
                                                                                                            #funciones para medir el tiempo de ejecución
def measure_all(length):
    generate_random_string_multi = generate_random_string_one(length)
    time1, _ = measure_execution_time(lambda s: palindrome_cuts_A(s), generate_random_string_multi)
    time2, _ = measure_execution_time(lambda s: palindrome_cuts_B(s), generate_random_string_multi)
    return (time1, time2)


#############################################################################################################

def main():
    current_random_string = None 
    firsttime = 0
    results_recursive = []
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    results_dynamic = []
    generated_strings = []
    random_str = None

    while True:
        if firsttime == 0:
            print("=======================================================================================   /\__/\ ")
            print("| Trabajo 2 - Analisis de Algoritmos                                                  |   (='.'=)") 
            print("| Integrante: Diego Cabezas ||| Sección: 411 ||| Profesor: Luis Hernan Herrera Becerra|   ('')_('')")           #Main-Menu principal
            print("=======================================================================================")
            jump_line()
        print("Menú de opciones:")
        void()
        print("1. Resolver el problema de partición de palíndromos con ambos algoritmos")
        print("2. Generar el grafico para comparar los tiempos [100-1000]")
        print("3. Salir")
        void()
        print("Nota: Te recomendamos ejecutar la opción 1 antes de la opción 2 para obtener resultados")
        jump_line()
        option = input("Seleccione una opción: ")
        jump_line()

#############################################################################################################

        if option == "1":
            firsttime = 1
            for size in sizes:
                s = generate_random_string_one(size)                                                        #Generar cadenas aleatorias
                generated_strings.append(s)
                
            with open('cadenas_option_1.txt', 'w') as f:
                for s in generated_strings:                                                                 #Se guardan las cadenas en un .txt
                    f.write(s + '\n')
            ####################################################################################################
                n=0         #variables para el arreglo de donde se guarda tiempo...
                i=0
                for s in generated_strings:
                    size = len(s)
                    print(f"\nCadena generada (tamaño {size}): {s}")
                    start_time = time.time()
                    cuts_recursive, partition_recursive = palindrome_cuts_A(s)                          #Imprimir resultados O(n^3)
                    results_recursive.append(time.time() - start_time)
                    print(f"Algoritmo O(n^3) -> Mínimo de cortes: {cuts_recursive}")
                    void()
                    print(f"Cadena con los cortes: {partition_recursive} \n \n con tiempo de ejecución: {results_recursive[i]} segundos")
                    i=i+1
                    jump_line()
                    start_time = time.time()
                    cuts_dynamic, partition_dynamic = palindrome_cuts_B(s)
                    results_dynamic.append(time.time() - start_time)
                    print(f"Algoritmo O(n^2) -> Mínimo de cortes: {cuts_dynamic}")                                   #Imprimir resultados O(n^2)
                    void()
                    print(f"Cadena con los cortes: {partition_dynamic} \n \nCon tiempo de ejecución: {results_dynamic[n]} segundos")
                    n=n+1
                    jump_line()
            ####################################################################################################
                jump_line()
                print("Tiempos ordenados de 100 a 1000:")
                void()
                print(f"\nTiempos de ejecución del algoritmo (O(n^3)): {results_recursive}")
                void()
                print(f"Tiempos de ejecución del algoritmo (O(n^2)): {results_dynamic}")                           #Imprimir tiempos de ejecución
                jump_line()
                save_name = "execution_times_option_1.txt"
                with open(save_name, "w") as file:
                    file.write("Tiempos ordenados de 100 a 1000:")
                    file.write(" ")
                    file.write(f"Tiempo de ejecucion del algoritmo O(n^3): {results_recursive} segundos\n")
                    file.write(f"Tiempo de ejecucion del algoritmo O(n^2): {results_dynamic} segundos\n")
                print(f"Tiempos de ejecución guardados en la carpeta local llamado [{save_name}]")
                jump_line()
            ####################################################################################################
                jump_line()

        #############################################################################################################
        elif option == "2":
            lengths = list(range(100, 1001, 100))
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
                        print(f'Error al medir {length}: {exc}')                                                #Generar grafico de comparación de tiempos

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

            # Leer los tiempos
            print("Tiempos de ejecución del algoritmo (O(n^3)): ", times1)
            print("Tiempos de ejecución del algoritmo (O(n^2)): ", times2)
        
        #############################################################################################################
        
        elif option == "3":
            break
        
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
            jump_line()

if __name__ == "__main__":
    main()
