#include <stdio.h>
#include <omp.h>

#define ARRAY_SIZE 10000000

int main()
{
    static int array[ARRAY_SIZE];   // static allocation to avoid stack overflow
    long long sum = 0;              // long long to prevent overflow

    // Initialize array
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        array[i] = i + 1;
    }

    // Parallel for WITH reduction -> correct and deterministic
    #pragma omp parallel for //reduction(+:sum)
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        sum += array[i];
    }

    printf("Sum with reduction: %lld\n", sum);
    return 0;
}