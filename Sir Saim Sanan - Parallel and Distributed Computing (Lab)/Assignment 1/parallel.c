#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ARRAY_SIZE 20000

static void parallelBubbleSort(int values[], int size, int *threadCount)
{
    int done = 0;
    int swapped = 0;

#pragma omp parallel shared(values, size, done, swapped, threadCount)
    {
#pragma omp single
        *threadCount = omp_get_num_threads();

        for (int phase = 0; phase < size && !done; phase++)
        {
            int start = phase % 2;

#pragma omp single
            swapped = 0;

#pragma omp for reduction(| : swapped)
            for (int index = start; index < size - 1; index += 2)
            {
                if (values[index] > values[index + 1])
                {
                    int temporary = values[index];
                    values[index] = values[index + 1];
                    values[index + 1] = temporary;
                    swapped = 1;
                }
            }

#pragma omp single
            {
                if (!swapped)
                {
                    done = 1;
                }
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
    int threadCount = 0;
    srand((unsigned int)rollNumber);

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        values[index] = rand();
    }

    double start = omp_get_wtime();
    parallelBubbleSort(values, ARRAY_SIZE, &threadCount);
    double end = omp_get_wtime();

    FILE *output = fopen("parallel out.txt", "w");
    if (output == NULL)
    {
        printf("Could not create parallel out.txt\n");
        return 1;
    }

    for (int index = 0; index < ARRAY_SIZE; index++)
    {
        fprintf(output, "%d\n", values[index]);
    }
    fclose(output);

    printf("roll number = %d\n", rollNumber);
    printf("input size = %d\n", ARRAY_SIZE);
    printf("parallel\n");
    printf("execution time = %.12f seconds\n", end - start);
    printf("first value = %d\n", values[0]);
    printf("last value = %d\n", values[ARRAY_SIZE - 1]);
    printf("threads = %d\n", threadCount);
    return 0;
}
