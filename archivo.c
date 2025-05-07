#include <stdio.h>

int main() {
    int arreglo[10, 20]; // Error: la sintaxis para declarar un arreglo es incorrecta, los elementos no deben ir separados por coma.
    int arreglo2[] = 10; // Error: el tamaño no es especificado correctamente, se debe usar corchetes para indicar el tamaño o un valor de inicialización.
    int arreglo3[3] = {1, 2}; // Error: el tamaño del arreglo es 3, pero solo se proporcionan 2 elementos.
    int arreglo4[5] = {1, 2, 3}; // Error: El arreglo tiene tamaño 5 pero se inicializa solo con 3 valores.

    return 0;
}
