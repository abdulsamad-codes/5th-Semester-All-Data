#include <stdio.h>
#include <omp.h>

#define ARRAY_SIZE 1000

int main()
{
    int array[ARRAY_SIZE];
    int sum = 0;

    // Initialize array
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        array[i] = i + 1;
    }

// Parallelize the loop to calculate sum
#pragma omp parallel
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        sum += array[i];
    }

    printf("Sum: %d\n", sum);
    return 0;
}