#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Semilla para generar números aleatorios
    srand(time(NULL));

    // Generar dos números aleatorios
    int num1 = rand() % 100;  // Número entre 0 y 99
    int num2 = rand() % 100;  // Número entre 0 y 99

    // Generar un operador aleatorio (+, -, *)
    char operador;
    int operadorIndex = rand() % 3;
    switch (operadorIndex) {
        case 0:
            operador = '+';
            break;
        case 1:
            operador = '-';
            break;
        case 2:
            operador = '*';
            break;
    }

    // Mostrar la operación y el resultado parcial
    printf("Operación: %d %c %d\n", num1, operador, num2);
    int resultado_parcial;

    switch (operador) {
        case '+':
            resultado_parcial = num1 + num2;
            break;
        case '-':
            resultado_parcial = num1 - num2;
            break;
        case '*':
            resultado_parcial = num1 * num2;
            break;
    }

    printf("Resultado parcial: %d\n", resultado_parcial);

    // Generar otro operador aleatorio y un número aleatorio
    operadorIndex = rand() % 3;
    switch (operadorIndex) {
        case 0:
            operador = '+';
            break;
        case 1:
            operador = '-';
            break;
        case 2:
            operador = '*';
            break;
    }

    int num3 = rand() % 100;  // Número entre 0 y 99

    // Mostrar la operación final y el resultado
    printf("Operación final: %d %c %d\n", resultado_parcial, operador, num3);
    int resultado_final;

    switch (operador) {
        case '+':
            resultado_final = resultado_parcial + num3;
            break;
        case '-':
            resultado_final = resultado_parcial - num3;
            break;
        case '*':
            resultado_final = resultado_parcial * num3;
            break;
    }

    printf("Resultado final: %d\n", resultado_final);

    return 0;
}
