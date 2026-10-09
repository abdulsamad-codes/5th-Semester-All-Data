#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ARRAY_SIZE 20000

static void firstParallelAttempt(int values[], int size)
{
#pragma omp parallel for
    for (int pass = 0; pass < size - 1; pass++)
    {
        for (int index = 0; index < size - pass - 1; index++)
        {
            if (values[index] > values[index + 1])
            {
                int temporary = values[index];
                values[index] = values[index + 1];
                values[index + 1] = temporary;
            }
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <roll_number>\n", argv[0]);
        return 1;
    }

    int rollNumber = atoi(argv[1]);
    int values[ARRAY_SIZE];
    srand((unsigned int)rollNumber);

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        values[index] = rand();
    }

    double start = omp_get_wtime();
    firstParallelAttempt(values, ARRAY_SIZE);
    double end = omp_get_wtime();

    printf("roll number = %d\n", rollNumber);
    printf("input size = %d\n", ARRAY_SIZE);
    printf("attempt\n");
    printf("execution time = %.12f seconds\n", end - start);
    printf("first value = %d\n", values[0]);
    printf("last value = %d\n", values[ARRAY_SIZE - 1]);

    int sorted = 1;
    for (int index = 1; index < ARRAY_SIZE; index++)
    {
        if (values[index - 1] > values[index])
        {
            sorted = 0;
            break;
        }
    }
    printf("sorted correctly = %s\n", sorted ? "yes" : "no");
    return 0;
}
